"""GATE Admin Portal: PDF splitter (download as ZIP) + GATE JSON importer."""
import io
import os
import re
import zipfile

import pandas as pd
import streamlit as st
from pypdf import PdfReader, PdfWriter

from webui import jobs
from webui.importers import import_gate_json, parse_json_upload
from webui.services import supabase
from webui.ui import log_action, page_header


def render():
    page_header("🎓  GATE Admin Portal", "gate")
    t1, t2 = st.tabs(["🗂  PDF Splitter", "📥  JSON Importer"])
    with t1:
        _tab_splitter()
    with t2:
        _tab_import()


def _safe_name(name: str) -> str:
    name = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", name.strip()).strip(". ")
    if not name:
        return ""
    return name if name.lower().endswith(".pdf") else name + ".pdf"


def split_pdf_to_zip(raw: bytes, ranges: list[tuple[str, int, int]]) -> bytes:
    """ranges: (file name, first page, last page) — 1-based, inclusive."""
    rdr = PdfReader(io.BytesIO(raw))
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, s, e in ranges:
            w = PdfWriter()
            for pn in range(s - 1, e):
                w.add_page(rdr.pages[pn])
            out = io.BytesIO()
            w.write(out)
            zf.writestr(name, out.getvalue())
    return buf.getvalue()


@st.cache_data(show_spinner=False, max_entries=4)
def _page_count(raw: bytes) -> int:
    return len(PdfReader(io.BytesIO(raw)).pages)


def _default_ranges(total: int) -> pd.DataFrame:
    return pd.DataFrame([{"File name": "Split_Part_1", "Start page": 1, "End page": total or 5}])


def _tab_splitter():
    with st.container(border=True):
        st.markdown("**Upload your GATE Question Bank PDF**")
        up = st.file_uploader("PDF file", type=["pdf"], key="pdf_src", label_visibility="collapsed")
    if not up:
        st.caption("📁  Select a PDF file to begin...")
        return
    raw = up.getvalue()
    try:
        total = _page_count(raw)
    except Exception as e:
        st.error(f"Failed to read PDF: {e}")
        return
    st.caption(f"📄  {up.name} ({total} pages)")

    # New file → fresh range table (desktop clears ranges on browse)
    sig = f"{up.name}:{len(raw)}:{total}"
    if st.session_state.get("pdf_sig") != sig or "pdf_ranges" not in st.session_state:
        st.session_state.pdf_sig = sig
        st.session_state.pop("pdf_zip", None)
        st.session_state.pdf_ranges = _default_ranges(total)
        st.session_state.pdf_editor_v = st.session_state.get("pdf_editor_v", 0) + 1

    with st.container(border=True):
        st.markdown("**Define Custom Splits**  ·  add rows with ➕ at the bottom of the table, delete by selecting a row and pressing 🗑")
        edited = st.data_editor(
            st.session_state.pdf_ranges, num_rows="dynamic", width="stretch", hide_index=True,
            key=f"pdf_editor_{st.session_state.pdf_editor_v}",
            column_config={
                "File name": st.column_config.TextColumn(required=True, default="Split_Part"),
                "Start page": st.column_config.NumberColumn(min_value=1, max_value=total, step=1, required=True, default=1),
                "End page": st.column_config.NumberColumn(min_value=1, max_value=total, step=1, required=True, default=total),
            },
        )
        c1, c2 = st.columns(2)
        if c1.button("🧹 Clear All", width="stretch"):
            st.session_state.pdf_ranges = _default_ranges(total)
            st.session_state.pdf_editor_v += 1
            st.rerun()
        run = c2.button("🚀 Process & Split PDF", type="primary", width="stretch")

    if run:
        parsed, errors, seen = [], [], set()
        rows = edited.to_dict("records")
        if not rows:
            errors.append("Must keep at least one split range.")
        for i, r in enumerate(rows, 1):
            name = _safe_name(str(r.get("File name") or ""))
            try:
                s, e = int(r.get("Start page")), int(r.get("End page"))
            except (TypeError, ValueError):
                errors.append(f"Invalid page numbers in Range #{i}.")
                continue
            if not name:
                errors.append(f"Range #{i} needs a file name.")
            elif name.lower() in seen:
                errors.append(f"Duplicate file name '{name}' (Range #{i}).")
            if not (1 <= s <= e <= total):
                errors.append(f"Range #{i}: pages must satisfy 1 ≤ start ≤ end ≤ {total}.")
            seen.add(name.lower())
            parsed.append((name, s, e))
        if errors:
            for msg in errors:
                st.error(msg)
            return
        try:
            zipped = split_pdf_to_zip(raw, parsed)
        except Exception as ex:
            st.error(f"Failed: {ex}")
            return
        st.session_state.pdf_zip = (os.path.splitext(up.name)[0] + "_splits.zip", zipped)
        log_action("SPLIT_PDF", content_type="gate_pdf", file_name=up.name,
                   details={"ranges": [f"{n}:{s}-{e}" for n, s, e in parsed]})
        st.success(f"Successfully split into {len(parsed)} PDF(s)! Download below.")

    z = st.session_state.get("pdf_zip")
    if z:
        st.download_button("⬇️  Download split PDFs (ZIP)", data=z[1], file_name=z[0],
                           mime="application/zip", type="primary")


def _tab_import():
    running = jobs.is_running("gate_import")
    with st.container(border=True):
        st.markdown("**Import GATE JSON into gate_questions**")
        up = st.file_uploader("Choose GATE JSON File", type=["json"], key="gj_file", disabled=running)
        if st.button("📂  Import GATE JSON", type="primary", disabled=running or not up):
            try:
                data = parse_json_upload(up.getvalue())
            except ValueError as e:
                st.error(str(e))
            else:
                log_action("IMPORT_GATE_JSON", content_type="gate_json",
                           subject=(data.get("subject") or {}).get("subject_name"), file_name=up.name)
                jobs.start_job("gate_import", import_gate_json, supabase(), data)
                st.rerun()
    with st.container(border=True):
        jobs.render_job_log("gate_import", "Import Log")
