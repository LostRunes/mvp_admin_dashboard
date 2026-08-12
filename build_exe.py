import os
import subprocess
import sys

print("[START] Building Cozy Study Hub & Resource Dashboard EXE...")
print(f"[INFO] Python: {sys.version}")

# First, generate a .spec file via pyi-makespec, then build from it
# This gives us full control and lets us use collect_all() for pydantic

spec_content = '''
# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_submodules, collect_data_files

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
             gotrue_datas + postgrest_datas + storage3_datas + httpx_datas + ctk_datas)
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
    name="Cozy_Study_Hub_Dashboard",
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
    name="Cozy_Study_Hub_Dashboard",
)
'''

spec_path = "Cozy_Study_Hub_Dashboard.spec"
with open(spec_path, "w") as f:
    f.write(spec_content)

print(f"[OK] Wrote {spec_path}")

# Now run PyInstaller with the spec file
command = [
    sys.executable, "-m", "PyInstaller",
    "--noconfirm",
    "--clean",
    spec_path
]

print(f"[RUN] {' '.join(command)}")
result = subprocess.run(command, text=True)

if result.returncode == 0:
    print("\n[SUCCESS] Build completed!")
    print("Your app is in: dist/Cozy_Study_Hub_Dashboard/")
    print("Share the entire 'Cozy_Study_Hub_Dashboard' folder or zip it up.")
else:
    print("\n[ERROR] Build failed with code:", result.returncode)
