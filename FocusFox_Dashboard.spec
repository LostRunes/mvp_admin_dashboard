# -*- mode: python ; coding: utf-8 -*-
# FocusFox Admin Dashboard — PyInstaller build spec
# Bundles: PySide6, supabase, firebase-admin, google-auth-oauthlib, imagekitio, pypdf

from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules
import os

# ── Collect packages that need full collection ────────────────────────────────
def _ca(pkg):
    try:
        d, b, h = collect_all(pkg)
        return d, b, h
    except Exception:
        return [], [], []

pydantic_d,     pydantic_b,     pydantic_h     = _ca("pydantic")
pydantic_core_d,pydantic_core_b,pydantic_core_h= _ca("pydantic_core")
supabase_d,     supabase_b,     supabase_h     = _ca("supabase")
gotrue_d,       gotrue_b,       gotrue_h       = _ca("gotrue")
postgrest_d,    postgrest_b,    postgrest_h    = _ca("postgrest")
storage3_d,     storage3_b,     storage3_h    = _ca("storage3")
httpx_d,        httpx_b,        httpx_h        = _ca("httpx")
firebase_d,     firebase_b,     firebase_h     = _ca("firebase_admin")
google_auth_d,  google_auth_b,  google_auth_h  = _ca("google.auth")
google_oauth_d, google_oauth_b, google_oauth_h = _ca("google_auth_oauthlib")
grpc_d,         grpc_b,         grpc_h         = _ca("grpc")
proto_d,        proto_b,        proto_h        = _ca("proto")
imagekit_d,     imagekit_b,     imagekit_h     = _ca("imagekitio")
pypdf_d,        pypdf_b,        pypdf_h        = _ca("pypdf")
dotenv_d,       dotenv_b,       dotenv_h       = _ca("dotenv")
requests_d,     requests_b,     requests_h     = _ca("requests")
urllib3_d,      urllib3_b,      urllib3_h      = _ca("urllib3")
certifi_d,      certifi_b,      certifi_h      = _ca("certifi")
charset_d,      charset_b,      charset_h      = _ca("charset_normalizer")

all_datas = (
    pydantic_d + pydantic_core_d +
    supabase_d + gotrue_d + postgrest_d + storage3_d + httpx_d +
    firebase_d + google_auth_d + google_oauth_d + grpc_d + proto_d +
    imagekit_d + pypdf_d + dotenv_d + requests_d + urllib3_d +
    certifi_d + charset_d +
    # Bundle the images folder
    [("images", "images")] +
    # Bundle config files that sit next to the exe
    [("credentials.json",              ".")] +
    [("firebase_service_account.json", ".")] +
    [(".env",                          ".")]
)

all_binaries = (
    pydantic_b + pydantic_core_b +
    supabase_b + gotrue_b + postgrest_b + storage3_b + httpx_b +
    firebase_b + google_auth_b + google_oauth_b + grpc_b + proto_b +
    imagekit_b + pypdf_b + dotenv_b + requests_b + urllib3_b +
    certifi_b + charset_b
)

all_hiddenimports = (
    pydantic_h + pydantic_core_h +
    supabase_h + gotrue_h + postgrest_h + storage3_h + httpx_h +
    firebase_h + google_auth_h + google_oauth_h + grpc_h + proto_h +
    imagekit_h + pypdf_h + dotenv_h + requests_h + urllib3_h +
    certifi_h + charset_h + [
    # PySide6
    "PySide6.QtWidgets", "PySide6.QtCore", "PySide6.QtGui",
    "PySide6.QtNetwork", "PySide6.QtPrintSupport",
    # Supabase transitive
    "anyio", "sniffio", "h11", "h2", "hyperframe", "hpack",
    # Firebase
    "google.cloud.firestore", "google.cloud.firestore_v1",
    "google.api_core", "google.auth.transport.requests",
    "google.oauth2.credentials", "google.oauth2.service_account",
    "google_auth_oauthlib.flow",
    "firebase_admin", "firebase_admin.credentials", "firebase_admin.firestore",
    # grpc
    "grpc", "grpc._channel", "grpc._utilities",
    # Misc
    "requests", "dotenv", "pypdf", "imagekitio",
    "threading", "json", "re", "io", "os",
    "firebase_auth",   # our custom module
])

a = Analysis(
    ["dashboard_app.py"],
    pathex=[os.path.abspath(".")],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=all_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "matplotlib", "numpy", "scipy", "pandas", "IPython", "jupyter",
        "notebook", "sphinx", "docutils", "pytest", "unittest",
        "tkinter", "customtkinter", "tensorflow", "keras", "torch",
        "mediapipe", "onnx", "tensorboard",
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="FocusFox_Dashboard",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,           # no terminal window popup
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="images/FocusFox_icon.png",  # use the fox icon
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="FocusFox_Dashboard",
)
