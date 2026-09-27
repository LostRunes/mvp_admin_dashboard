"""Admin-only: approve / reject / revoke dashboard access requests."""
import html

import streamlit as st

from webui.config import _email_set, admin_emails
from webui.firebase import FirebaseError
from webui.ui import fb, flash, log_action, show_flash

STATUS_BADGE = {"pending": "🟡 Pending", "approved": "🟢 Approved",
                "rejected": "🔴 Rejected", "revoked": "⚫ Revoked"}


def pending_count() -> int:
    """Cheap badge count for the sidebar (cached per session for 60 s)."""
    import time
    cache = st.session_state.get("_acc_badge")
    if cache and cache[0] > time.time():
        return cache[1]
    n = 0
    try:
        n = sum(1 for r in fb().list_access_requests() if r.get("status") == "pending")
    except Exception:
        pass
    st.session_state._acc_badge = (time.time() + 60, n)
    return n


def _act(uid, status, email):
    try:
        if status == "delete":
            fb().delete_access_request(uid)
        else:
            fb().set_access_status(uid, status)
    except FirebaseError as e:
        flash(str(e), "error")
        return
    log_action(f"ACCESS_{status.upper()}", content_type="dashboard_access", subject=email, content_id=uid)
    st.session_state.pop("_acc_badge", None)
    flash({"approved": f"Approved {email}.", "rejected": f"Rejected {email}.",
           "revoked": f"Revoked access for {email}.",
           "delete": f"Removed {email}'s record — they can request again."}[status])


def render():
    col_t, col_r = st.columns([6, 1], vertical_alignment="center")
    col_t.markdown("## 👥  Access Requests")
    if col_r.button("🔄 Refresh", width="stretch"):
        st.rerun()
    show_flash()
    if not fb():
        st.error("Firestore sync is unavailable for this session, so requests can't be loaded.")
        return
    try:
        reqs = fb().list_access_requests()
    except FirebaseError as e:
        st.error(str(e))
        return

    groups = {s: [r for r in reqs if r.get("status") == s] for s in STATUS_BADGE}
    t_p, t_a, t_o = st.tabs([f"🟡 Pending ({len(groups['pending'])})",
                             f"🟢 Approved ({len(groups['approved'])})",
                             f"🔴 Rejected / Revoked ({len(groups['rejected']) + len(groups['revoked'])})"])
    with t_p:
        _rows(groups["pending"], [("✅ Approve", "approved", "primary"), ("❌ Reject", "rejected", "secondary")],
              "No pending requests.")
    with t_a:
        _rows(groups["approved"], [("⛔ Revoke", "revoked", "secondary")], "Nobody approved via requests yet.")
    with t_o:
        _rows(groups["rejected"] + groups["revoked"],
              [("✅ Approve", "approved", "primary"), ("🗑 Let them re-request", "delete", "secondary")],
              "Nothing here.")

    with st.expander("Always-allowed accounts (from server secrets)"):
        static = sorted(_email_set("ALLOWED_EMAILS"))
        st.markdown("**Admins:** " + ", ".join(sorted(admin_emails())) + "  \n**Allowed:** " +
                    (", ".join(static) or "—"))
        st.caption("Change these in Streamlit Cloud → app → Settings → Secrets "
                   "(ALLOWED_EMAILS / ADMIN_EMAILS). New admins must also be added to firestore.rules.")


def _rows(rows, actions, empty):
    if not rows:
        st.caption(empty)
        return
    for r in rows:
        uid, email = r.get("_id"), r.get("email", "")
        with st.container(border=True):
            c1, *btns = st.columns([5] + [1.4] * len(actions), vertical_alignment="center")
            note = r.get("note") or ""
            extra = f"<br><i>“{html.escape(note)}”</i>" if note else ""
            decided = (f"<br><span class='ff-muted'>{STATUS_BADGE.get(r.get('status'), '')} by "
                       f"{html.escape(str(r.get('decided_by')))} · {html.escape(str(r.get('decided_at', ''))[:16])}</span>"
                       if r.get("decided_by") else "")
            c1.markdown(f"<b>{html.escape(str(r.get('name') or 'Unknown'))}</b> · {html.escape(email)}"
                        f"<br><span class='ff-muted'>requested {html.escape(str(r.get('requested_at', ''))[:16])}"
                        f"</span>{extra}{decided}", unsafe_allow_html=True)
            for col, (label, status, kind) in zip(btns, actions):
                col.button(label, key=f"acc_{status}_{uid}", type=kind, width="stretch",
                           on_click=_act, args=(uid, status, email))
