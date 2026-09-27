"""Secret / setting lookup: Streamlit secrets first, then environment (.env for local runs).

Nothing sensitive is hardcoded here — a missing required secret stops the app with a
clear message instead of silently falling back to a baked-in key.
"""
import os

import streamlit as st
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, "images")

load_dotenv(os.path.join(BASE_DIR, ".env"))


def get_secret(name: str, default=None):
    try:
        if name in st.secrets:
            return st.secrets[name]
    except Exception:
        # No secrets.toml at all (e.g. local run using only .env)
        pass
    val = os.getenv(name)
    return val if val not in (None, "") else default


def require_secret(name: str) -> str:
    val = get_secret(name)
    if not val:
        st.error(
            f"Server is missing the **{name}** secret. Add it in the Streamlit Cloud "
            "app settings → Secrets (or `.streamlit/secrets.toml` locally)."
        )
        st.stop()
    return val


def _email_set(name: str) -> set[str]:
    """A TOML list or a comma-separated string of emails."""
    raw = get_secret(name, [])
    if isinstance(raw, str):
        raw = raw.split(",")
    return {str(e).strip().lower() for e in raw if str(e).strip()}


def admin_emails() -> set[str]:
    """Admins can always sign in and approve access requests (must match firestore.rules)."""
    return _email_set("ADMIN_EMAILS")


def allowed_emails() -> set[str]:
    """Always-allowed accounts (admins included); everyone else must request access."""
    return _email_set("ALLOWED_EMAILS") | admin_emails()


def img_path(name: str) -> str | None:
    """Resolve an image in images/ by bare file name only (no path traversal)."""
    if not name:
        return None
    p = os.path.join(IMAGES_DIR, os.path.basename(str(name)))
    return p if os.path.isfile(p) else None
