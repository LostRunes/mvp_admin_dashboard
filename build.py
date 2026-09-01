"""
build.py — Build FocusFox Dashboard into a distributable exe + folder
Run:  python build.py

Output: dist/FocusFox_Dashboard/   ← share this folder or zip it
"""
import os
import sys
import shutil
import subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(BASE, "FocusFox_Dashboard.spec")
DIST = os.path.join(BASE, "dist", "FocusFox_Dashboard")

# ── Pre-flight checks ─────────────────────────────────────────────────────────
required = ["credentials.json", "firebase_service_account.json", ".env", "images"]
missing  = [f for f in required if not os.path.exists(os.path.join(BASE, f))]
if missing:
    print(f"[ERROR] Missing required files: {missing}")
    sys.exit(1)

# ── Install PyInstaller if needed ─────────────────────────────────────────────
try:
    import PyInstaller
except ImportError:
    print("[INFO] Installing PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

# ── Write Spec file dynamically ───────────────────────────────────────────────
spec_content = '''# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# Collect all pydantic and supabase (including compiled extensions)
pydantic_datas, pydantic_binaries, pydantic_hiddenimports = collect_all("pydantic")
pydantic_core_datas, pydantic_core_binaries, pydantic_core_hiddenimports = collect_all("pydantic_core")
supabase_datas, supabase_binaries, supabase_hiddenimports = collect_all("supabase")
supabauth_datas, supabauth_binaries, supabauth_hiddenimports = collect_all("supabase_auth")
gotrue_datas, gotrue_binaries, gotrue_hiddenimports = collect_all("gotrue")
postgrest_datas, postgrest_binaries, postgrest_hiddenimports = collect_all("postgrest")
storage3_datas, storage3_binaries, storage3_hiddenimports = collect_all("storage3")
httpx_datas, httpx_binaries, httpx_hiddenimports = collect_all("httpx")
ctk_datas, ctk_binaries, ctk_hiddenimports = collect_all("customtkinter")

all_datas = (pydantic_datas + pydantic_core_datas + supabase_datas + supabauth_datas +
             gotrue_datas + postgrest_datas + storage3_datas + httpx_datas + ctk_datas +
             [("credentials.json", "."), ("firebase_service_account.json", "."), (".env", "."), ("images", "images")])
all_binaries = (pydantic_binaries + pydantic_core_binaries + supabase_binaries +
                supabauth_binaries + gotrue_binaries + postgrest_binaries +
                storage3_binaries + httpx_binaries + ctk_binaries)
all_hiddenimports = (pydantic_hiddenimports + pydantic_core_hiddenimports +
                     supabase_hiddenimports + supabauth_hiddenimports +
                     gotrue_hiddenimports + postgrest_hiddenimports +
                     storage3_hiddenimports + httpx_hiddenimports + ctk_hiddenimports +
                     ["PIL._imagingtk", "PIL.Image", "pypdf", "requests", "dotenv",
                      "imagekitio", "tkinter", "tkinter.filedialog", "tkinter.messagebox",
                      "re", "json", "threading", "io"])

a = Analysis(
    ["dashboard_app.py"],
    pathex=[],
    binaries=all_binaries,
    datas=all_datas,
    hiddenimports=all_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["matplotlib", "numpy", "scipy", "pandas", "IPython", "jupyter",
               "notebook", "sphinx", "docutils", "pytest", "unittest",
               "email.mime", "xml.etree"],
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
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
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
'''

with open(SPEC, "w", encoding="utf-8") as f:
    f.write(spec_content)
print(f"[OK] Generated {SPEC}")

# ── Run the build ─────────────────────────────────────────────────────────────
print("\n" + "="*60)
print("  FocusFox Dashboard — Building EXE")
print("="*60)
cmd = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", SPEC]
print(f"[RUN] {' '.join(cmd)}\n")
result = subprocess.run(cmd, cwd=BASE)

if result.returncode != 0:
    print("\n[ERROR] Build failed. Check the output above.")
    sys.exit(result.returncode)

# ── Copy assets and configs into the build folder ────────────────────────────
print("\n[COPY] Copying assets and configurations into build folder...")
for item in required:
    src = os.path.join(BASE, item)
    dst = os.path.join(DIST, item)
    if os.path.isdir(src):
        if os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    else:
        shutil.copy2(src, dst)
print("[OK] Assets copied successfully.")

# ── Create zip for sharing ────────────────────────────────────────────────────
print("\n[ZIP] Creating FocusFox_Dashboard.zip...")
zip_path = os.path.join(BASE, "dist", "FocusFox_Dashboard")
shutil.make_archive(zip_path, "zip", os.path.join(BASE, "dist"), "FocusFox_Dashboard")
final_zip = zip_path + ".zip"
size_mb   = os.path.getsize(final_zip) / (1024 * 1024)

print("\n" + "="*60)
print("  [OK] Build Complete!")
print("="*60)
print(f"  EXE folder : dist/FocusFox_Dashboard/")
print(f"  ZIP file   : dist/FocusFox_Dashboard.zip  ({size_mb:.1f} MB)")
print()
print("  [INFO] Share the ZIP file with your developers.")
print("  They just extract it and run FocusFox_Dashboard.exe")
print("  No Python installation required!")
print("="*60)
