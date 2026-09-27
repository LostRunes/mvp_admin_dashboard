"""FocusFox Admin — web edition of dashboard_app.py.

Run locally:   streamlit run web_app.py
Deploy:        Streamlit Community Cloud → main file `web_app.py` (see .streamlit/secrets.toml.example)
"""
import html
import time

import streamlit as st

from webui.config import allowed_emails, get_secret, img_path

st.set_page_config(
    page_title="FocusFox Admin",
    page_icon=img_path("focus_fox_nobg.png") or "🦊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from webui.firebase import FirebaseError, FirebaseSession, jwt_payload  # noqa: E402
from webui.services import supabase_online  # noqa: E402
from webui.ui import apply_css, log_action  # noqa: E402

VERSION = "v2.0.0  •  Web"
NAV = [
    ("guide", "🏠", "Home Menu"),
    ("yt", "📺", "College PYQ"),
    ("gate", "🎓", "GATE Portal"),
    ("college_img", "🖼️", "College Images"),
    ("gate_img", "📐", "GATE Images"),
    ("gate_db", "📁", "GATE DB Editor"),
    ("todo", "📝", "Developer Tasks"),
    ("spotify", "🎵", "Focus Music"),
]

apply_css()


def _auth_configured() -> bool:
    try:
        return "auth" in st.secrets
    except Exception:
        return False


def _centered():
    return st.columns([1, 1.3, 1])[1]


def login_screen():
    with _centered(), st.container(border=True):
        if img_path("focus_fox_nobg.png"):
            st.image(img_path("focus_fox_nobg.png"), width=72)
        st.markdown("## FocusFox Admin")
        st.caption("Sign in with Google to continue")
        if not _auth_configured():
            st.error("Google sign-in is not configured on this server (missing `[auth]` secrets).")
            return
        if st.button("🔑  Sign in with Google", type="primary", width="stretch"):
            st.login()


def denied_screen(email: str, reason: str):
    with _centered(), st.container(border=True):
        st.markdown("## 🔒 Access denied")
        st.write(reason)
        st.caption(f"Signed in as {email or 'unknown account'}")
        if st.button("Sign out", width="stretch"):
            st.logout()


def sign_out():
    log_action("LOGOUT")
    st.session_state.clear()
    st.logout()


# ── 1. Google sign-in ─────────────────────────────────────────────────────────
if not st.user.is_logged_in:
    login_screen()
    st.stop()

# ── 2. Allow-list (fail closed) ───────────────────────────────────────────────
email = str(st.user.get("email") or "").strip().lower()
allowed = allowed_emails()
if not allowed:
    denied_screen(email, "No developer accounts are allow-listed on this server yet "
                         "(ALLOWED_EMAILS secret is empty), so nobody can use the dashboard.")
    st.stop()
if st.user.get("email_verified") not in (True, "true") or email not in allowed:
    denied_screen(email, "This Google account is not on the FocusFox developer allow-list. "
                         "Ask an admin to add your email.")
    st.stop()

# ── 3. Firebase identity (same UID as the desktop app) ────────────────────────
if "fb" not in st.session_state:
    google_token = st.user.tokens.get("id") if st.user.tokens else None
    if google_token and jwt_payload(google_token).get("exp", 0) < time.time() + 30:
        # Google ID tokens live 1h; the sign-in cookie lives longer. Ask for a fresh sign-in
        # (same as the desktop, which signs in every launch) so audit logging never silently stops.
        st.session_state.clear()
        st.logout()
        st.stop()
    try:
        if not google_token:
            raise FirebaseError("Google ID token not exposed — set expose_tokens = [\"id\"] under [auth].")
        session = FirebaseSession(get_secret("FIREBASE_WEB_API_KEY"), google_token,
                                  fallback_name=st.user.get("name") or "", fallback_email=email)
        session.upsert_user()
        session.log_action("LOGIN")
        st.session_state.fb = session
        st.session_state.fb_error = None
    except (FirebaseError, Exception) as e:
        print(f"[FirebaseAuth] {e}")
        st.session_state.fb = None
        st.session_state.fb_error = str(e)

if "page" not in st.session_state:
    st.session_state.page = "guide"


def go(key: str):
    st.session_state.page = key


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="ff-sb-head">FOCUSFOX.EXE</div>', unsafe_allow_html=True)
    st.caption("✦ Admin Workspace ✦")
    st.divider()
    st.caption("PROGRAMS")
    for key, icon, label in NAV:
        st.button(f"{icon}  {label}", key=f"nav_{key}", on_click=go, args=(key,), width="stretch",
                  type="primary" if st.session_state.page == key else "tertiary")
    st.divider()
    st.markdown(f"<b>👤  {html.escape(str(st.user.get('name') or 'Developer'))}</b><br>"
                f"<span class='ff-muted'>{html.escape(email)}</span>", unsafe_allow_html=True)
    if supabase_online():
        st.markdown(":green[☁  Connected]")
    else:
        st.markdown(":red[☁  Offline]")
    if st.session_state.get("fb") is None:
        st.markdown(":orange[☁  Firestore sync offline]", help=st.session_state.get("fb_error") or None)
    st.caption("🌗 Theme: ⋮ menu (top right) → Settings")
    if st.button("🚪  Sign out", width="stretch"):
        sign_out()
    st.caption(VERSION)

# ── Pages ─────────────────────────────────────────────────────────────────────
page = st.session_state.page
if page == "guide":
    from webui.views import home
    home.render(go)
elif page == "yt":
    from webui.views import college
    college.render()
elif page == "gate":
    from webui.views import gate
    gate.render()
elif page == "college_img":
    from webui.views import images
    images.render_college()
elif page == "gate_img":
    from webui.views import images
    images.render_gate()
elif page == "gate_db":
    from webui.views import gate_db
    gate_db.render(email)
elif page == "todo":
    from webui.views import personal
    personal.render_todo()
elif page == "spotify":
    from webui.views import personal
    personal.render_spotify()
