"""Shared look & feel, page headers, help dialog, flash messages and audit logging."""
import html
import re

import streamlit as st

from webui.config import get_secret, img_path
from webui.firebase import DEFAULT_PROJECT_ID, fetch_guide
from webui.help_content import HELP

PALETTES = {
    "dark": {"card": "rgba(40, 36, 68, 0.82)", "border": "#5C53A3", "text": "#E8E2FF",
             "muted": "#8D89A5", "pink": "#F3A6C3", "tip_bg": "rgba(18, 32, 21, 0.85)",
             "tip_border": "#2E7D32", "bg_img": "dark_deskbg2.jpg", "bg": "#1C1B29"},
    "light": {"card": "rgba(255, 253, 253, 0.85)", "border": "#8174D6", "text": "#5C5874",
              "muted": "#8D89A5", "pink": "#F3A6C3", "tip_bg": "rgba(230, 244, 234, 0.92)",
              "tip_border": "#A3E635", "bg_img": "light_bg.jpg", "bg": "#DDEFFF"},
}


def theme_mode() -> str:
    try:
        t = st.context.theme.type
        return t if t in PALETTES else "dark"
    except Exception:
        return "dark"


def apply_css():
    c = PALETTES[theme_mode()]
    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400;600;700&display=swap');
.stApp {{
    background: linear-gradient({c['bg']}99, {c['bg']}99), url('app/static/{c['bg_img']}') center / cover fixed, {c['bg']};
}}
h1, h2, h3, .ff-title {{ font-family: 'Pixelify Sans', 'Courier New', sans-serif !important; }}
[data-testid="stVerticalBlockBorderWrapper"] {{ background: {c['card']}; border-radius: 10px; }}
.ff-card {{ background: {c['card']}; border: 2px solid {c['border']}; border-radius: 10px;
            padding: 14px 16px; margin-bottom: 10px; color: {c['text']}; }}
.ff-tip {{ background: {c['tip_bg']}; border: 2px solid {c['tip_border']}; border-radius: 10px;
           padding: 14px 16px; color: {c['text']}; }}
.ff-guide {{ white-space: pre-wrap; font-size: 0.92rem; line-height: 1.5; }}
.ff-guide a {{ color: {c['pink']}; text-decoration: underline; }}
.ff-done {{ color: {c['muted']}; text-decoration: line-through; }}
.ff-muted {{ color: {c['muted']}; font-size: 0.8rem; }}
.ff-sb-head {{ background: {c['pink']}; color: #1C1B29; border-radius: 6px; padding: 8px 12px;
               font-family: 'Pixelify Sans', sans-serif; font-weight: 700; letter-spacing: 1px; }}
</style>""", unsafe_allow_html=True)


# ── flash messages (survive one st.rerun) ─────────────────────────────────────
def flash(msg: str, kind: str = "success"):
    st.session_state.setdefault("_flash", []).append((kind, msg))


def show_flash():
    for kind, msg in st.session_state.pop("_flash", []):
        {"success": st.success, "error": st.error, "warning": st.warning, "info": st.info}[kind](msg)


# ── audit log ─────────────────────────────────────────────────────────────────
def fb():
    return st.session_state.get("fb")


def log_action(action: str, **kw):
    session = fb()
    if session:
        session.log_action(action, **kw)


# ── help dialog ───────────────────────────────────────────────────────────────
@st.cache_data(ttl=600, show_spinner=False)
def _load_guide(key: str) -> dict | None:
    return fetch_guide(key, get_secret("FIREBASE_WEB_API_KEY"),
                       get_secret("FIREBASE_PROJECT_ID", DEFAULT_PROJECT_ID))


def format_guide_html(text: str) -> str:
    esc = html.escape(str(text))
    return re.sub(r'(https?://[^\s<>"]+)',
                  r'<a href="\1" target="_blank" rel="noopener noreferrer">\1</a>', esc)


@st.dialog("Help Guide", width="large")
def _help_dialog(key: str):
    fallback = HELP.get(key, {"title": f"Help Guide ({key})", "text": "No guide available.",
                              "image": "fox_happy.png", "schema": "Database schema offline."})
    with st.spinner("Fetching detailed guidelines and database schema from Firestore..."):
        data = _load_guide(key) or fallback
    col_i, col_t = st.columns([1, 6], vertical_alignment="center")
    p = img_path(data.get("image") or "fox_happy.png") or img_path("fox_happy.png")
    if p:
        col_i.image(p, width=60)
    col_t.markdown(f"### {html.escape(str(data.get('title', 'Guide')))}", unsafe_allow_html=True)
    full = str(data.get("text", ""))
    if data.get("schema"):
        full += "\n\n" + "=" * 50 + "\n" + str(data["schema"])
    st.markdown(f'<div class="ff-guide">{format_guide_html(full)}</div>', unsafe_allow_html=True)
    if st.button("Got it!", type="primary"):
        st.rerun()


def page_header(title: str, key: str):
    col_t, col_h = st.columns([6, 1], vertical_alignment="center")
    col_t.markdown(f"## {title}")
    if col_h.button("❓ Help", key=f"help_{key}", width="stretch"):
        _help_dialog(key)
    show_flash()


def mascot(name: str, width: int = 56):
    p = img_path(name)
    if p:
        st.image(p, width=width)
