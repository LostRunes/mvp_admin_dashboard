"""Shared Supabase + ImageKit clients and small DB helpers."""
import io
import os
import re

import streamlit as st
from PIL import Image

from webui.config import get_secret, require_secret

ALLOWED_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


@st.cache_resource(show_spinner=False)
def _supabase_client(url: str, key: str):
    from supabase import create_client
    return create_client(url, key)


def supabase():
    url = require_secret("SUPABASE_URL")
    # Prefer a server-only service-role key when configured (lets you lock the anon
    # key down to read-only with RLS); otherwise use the same key as the desktop app.
    key = get_secret("SUPABASE_SERVICE_ROLE_KEY") or require_secret("SUPABASE_KEY")
    return _supabase_client(url, key)


@st.cache_data(ttl=60, show_spinner=False)
def supabase_online() -> bool:
    try:
        supabase().table("branches").select("id").limit(1).execute()
        return True
    except Exception:
        return False


@st.cache_resource(show_spinner=False)
def _imagekit_client(private_key: str):
    from imagekitio import ImageKit
    return ImageKit(private_key=private_key)


def imagekit_upload(data: bytes, file_name: str, folder: str) -> str:
    """Upload bytes to ImageKit (same call as the standalone uploaders). Returns CDN URL."""
    ik = _imagekit_client(require_secret("IMAGEKIT_PRIVATE_KEY"))
    kwargs = {}
    pub = get_secret("IMAGEKIT_PUBLIC_KEY")
    if pub:
        kwargs["public_key"] = pub
    res = ik.files.upload(
        file=data,
        file_name=file_name,
        folder=folder,
        use_unique_file_name=False,
        **kwargs,
    )
    if not getattr(res, "url", None):
        raise RuntimeError(f"ImageKit returned no URL for {file_name}")
    return res.url


def validate_image(uploaded) -> tuple[bytes, str]:
    """Return (bytes, lowercase ext) for an uploaded image, or raise ValueError."""
    name = uploaded.name or ""
    ext = os.path.splitext(name)[1].lower()
    if ext not in ALLOWED_IMAGE_EXTS:
        raise ValueError(f"{name}: unsupported file type (use PNG/JPG/JPEG/WEBP).")
    data = uploaded.getvalue()
    try:
        Image.open(io.BytesIO(data)).verify()
    except Exception:
        raise ValueError(f"{name}: file is not a valid image.") from None
    return data, ext


def natural_key(value) -> list:
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", str(value))]


def friendly_error(e: Exception) -> str:
    """Readable message for Supabase/PostgREST and other errors."""
    msg = getattr(e, "message", None)
    if msg:
        code = getattr(e, "code", None)
        return f"{msg} (code {code})" if code else str(msg)
    return str(e) or e.__class__.__name__


# ── Cached lookups (cleared after writes) ─────────────────────────────────────
@st.cache_data(ttl=120, show_spinner=False)
def load_subjects() -> list:
    r = supabase().table("subjects").select("id,name,code,yt_links").order("name").execute()
    return r.data or []


@st.cache_data(ttl=120, show_spinner=False)
def load_branches() -> list:
    return supabase().table("branches").select("id,name").order("name").execute().data or []


@st.cache_data(ttl=120, show_spinner=False)
def load_years() -> list:
    return supabase().table("years").select("id,name").order("name").execute().data or []


def clear_college_caches():
    load_subjects.clear()
    load_branches.clear()
    load_years.clear()


def subject_label(s: dict) -> str:
    return f"{s.get('name')} ({s.get('code')})"
