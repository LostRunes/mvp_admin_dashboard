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

# ── Create zip for sharing ────────────────────────────────────────────────────
print("\n[ZIP] Creating FocusFox_Dashboard.zip...")
zip_path = os.path.join(BASE, "dist", "FocusFox_Dashboard")
shutil.make_archive(zip_path, "zip", os.path.join(BASE, "dist"), "FocusFox_Dashboard")
final_zip = zip_path + ".zip"
size_mb   = os.path.getsize(final_zip) / (1024 * 1024)

print("\n" + "="*60)
print("  ✅  Build Complete!")
print("="*60)
print(f"  EXE folder : dist/FocusFox_Dashboard/")
print(f"  ZIP file   : dist/FocusFox_Dashboard.zip  ({size_mb:.1f} MB)")
print()
print("  📦 Share the ZIP file with your developers.")
print("  They just extract it and run FocusFox_Dashboard.exe")
print("  No Python installation required!")
print("="*60)
