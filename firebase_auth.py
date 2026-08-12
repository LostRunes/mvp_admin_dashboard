"""
firebase_auth.py — Google Auth + Firestore activity logger for FocusFox Desktop
Uses:
  - google-auth-oauthlib  → opens browser-based Google login
  - Firebase REST API     → exchanges Google ID token for Firebase identity
  - firebase-admin SDK    → writes activity logs to Firestore (bypasses security rules)
"""

import os
import json
import datetime
import threading
import requests

# ── Optional imports ─────────────────────────────────────────────────────────
try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.oauth2.credentials import Credentials
    _google_auth_ok = True
except ImportError:
    _google_auth_ok = False

try:
    import firebase_admin
    from firebase_admin import credentials as fb_credentials, firestore
    _firebase_admin_ok = True
except ImportError:
    _firebase_admin_ok = False

# ── Constants ─────────────────────────────────────────────────────────────────
BASE_DIR          = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH  = os.path.join(BASE_DIR, "credentials.json")
SERVICE_ACCT_PATH = os.path.join(BASE_DIR, "firebase_service_account.json")
TOKEN_CACHE_PATH  = os.path.join(BASE_DIR, ".firebase_token_cache.json")

# The Web API key from your Firebase project
# (same one visible in the Firebase console → Project Settings → General → Web API key)
FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY", "")

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]

# ── Module-level state ────────────────────────────────────────────────────────
_current_user: dict | None = None  # {"uid", "email", "name", "photo_url"}
_db = None                          # Firestore client


# ── Firestore init ────────────────────────────────────────────────────────────
def _init_firestore() -> bool:
    """Initialize firebase-admin if service account exists. Returns True on success."""
    global _db
    if _db is not None:
        return True
    if not _firebase_admin_ok:
        return False
    if not os.path.exists(SERVICE_ACCT_PATH):
        return False
    try:
        if not firebase_admin._apps:
            cred = fb_credentials.Certificate(SERVICE_ACCT_PATH)
            firebase_admin.initialize_app(cred)
        _db = firestore.client()
        return True
    except Exception as e:
        print(f"[FirebaseAuth] Firestore init failed: {e}")
        return False


# ── Google OAuth flow ─────────────────────────────────────────────────────────
def _google_sign_in() -> dict | None:
    """
    Opens the system browser for Google Sign-In.
    Returns a dict with Google user info + id_token, or None on failure.
    """
    if not _google_auth_ok:
        raise RuntimeError("google-auth-oauthlib is not installed. Run: pip install google-auth-oauthlib")
    if not os.path.exists(CREDENTIALS_PATH):
        raise FileNotFoundError(f"credentials.json not found at {CREDENTIALS_PATH}")

    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, scopes=SCOPES)
    google_creds: Credentials = flow.run_local_server(port=0, open_browser=True)

    # Fetch profile info from Google
    userinfo_resp = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {google_creds.token}"},
        timeout=10,
    )
    userinfo = userinfo_resp.json()
    userinfo["id_token"] = google_creds.id_token
    return userinfo


def _exchange_with_firebase(google_id_token: str) -> dict | None:
    """
    Sends the Google ID token to Firebase's signInWithIdp REST endpoint.
    Returns Firebase user dict or None.
    """
    if not FIREBASE_WEB_API_KEY:
        return None  # skip Firebase exchange if no web key; still return Google identity
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp?key={FIREBASE_WEB_API_KEY}"
    payload = {
        "requestUri": "http://localhost",
        "postBody": f"id_token={google_id_token}&providerId=google.com",
        "returnSecureToken": True,
        "returnIdpCredential": True,
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        data = resp.json()
        if "error" in data:
            print(f"[FirebaseAuth] Firebase exchange error: {data['error']}")
            return None
        return data  # has localId (Firebase UID), email, displayName, idToken
    except Exception as e:
        print(f"[FirebaseAuth] Firebase exchange request failed: {e}")
        return None


# ── Public API ────────────────────────────────────────────────────────────────
def login() -> dict | None:
    """
    Full Google → Firebase login flow.
    Returns current_user dict:
      { "uid", "email", "name", "photo_url" }
    Raises RuntimeError / FileNotFoundError on setup problems.
    """
    global _current_user

    google_info = _google_sign_in()
    if not google_info:
        return None

    firebase_info = _exchange_with_firebase(google_info.get("id_token", ""))

    if firebase_info:
        uid       = firebase_info.get("localId", google_info.get("id", "unknown"))
        email     = firebase_info.get("email", google_info.get("email", ""))
        name      = firebase_info.get("displayName", google_info.get("name", ""))
        photo_url = firebase_info.get("photoUrl", google_info.get("picture", ""))
    else:
        # Fallback: use Google identity directly (still unique by Google sub)
        uid       = google_info.get("id", "google_" + google_info.get("email", "unknown"))
        email     = google_info.get("email", "")
        name      = google_info.get("name", "")
        photo_url = google_info.get("picture", "")

    _current_user = {
        "uid":       uid,
        "email":     email,
        "name":      name,
        "photo_url": photo_url,
    }

    # Upsert user document
    _upsert_user()

    # Log LOGIN action
    log_action("LOGIN")

    return _current_user


def current_user() -> dict | None:
    """Returns the currently logged-in user dict, or None."""
    return _current_user


def logout():
    """Logs LOGOUT action and clears session."""
    global _current_user
    if _current_user:
        log_action("LOGOUT")
    _current_user = None


# ── Activity logging ──────────────────────────────────────────────────────────
def log_action(
    action: str,
    content_type: str | None = None,
    subject: str | None = None,
    topic: str | None = None,
    content_id: str | None = None,
    file_name: str | None = None,
    details: dict | None = None,
):
    """
    Write an activity log record to Firestore (non-blocking, fire-and-forget).
    Also always prints locally as a fallback.

    Actions:  LOGIN, LOGOUT, UPLOAD, EDIT, DELETE, IMPORT, SPLIT_PDF, ...
    """
    if not _current_user:
        return

    record = {
        "user_id":      _current_user.get("uid"),
        "user_email":   _current_user.get("email"),
        "user_name":    _current_user.get("name"),
        "action":       action,
        "content_type": content_type,
        "subject":      subject,
        "topic":        topic,
        "content_id":   str(content_id) if content_id else None,
        "file_name":    file_name,
        "details":      details or {},
        "timestamp_local": datetime.datetime.utcnow().isoformat() + "Z",
    }

    ts_str = record["timestamp_local"]
    print(f"[ActivityLog] {_current_user['name']} | {action} | {content_type or '-'} | {subject or '-'} @ {ts_str}")

    # Write to Firestore in background thread
    def _write():
        if not _init_firestore():
            return
        try:
            doc = dict(record)
            doc["timestamp"] = firestore.SERVER_TIMESTAMP
            _db.collection("activity_logs").add(doc)
        except Exception as e:
            print(f"[ActivityLog] Firestore write failed: {e}")

    threading.Thread(target=_write, daemon=True).start()


def get_guide(key: str) -> dict | None:
    """Fetches a guide document from Firestore, or returns None."""
    if not _init_firestore():
        return None
    try:
        doc = _db.collection("info_guides").document(key).get()
        if doc.exists:
            return doc.to_dict()
    except Exception as e:
        print(f"[FirebaseAuth] Fetch guide failed: {e}")
    return None


def get_todos() -> list:
    """Fetches the list of to-do items for the logged-in user."""
    if not _current_user or not _init_firestore():
        return []
    try:
        uid = _current_user["uid"]
        # Use order_by with a direction to be explicit; catch index errors gracefully
        try:
            docs = _db.collection("users").document(uid).collection("todos") \
                      .order_by("created_at").stream()
            items = [{"id": d.id, **d.to_dict()} for d in docs]
        except Exception:
            # Fallback: no ordering (e.g. index not built yet)
            docs = _db.collection("users").document(uid).collection("todos").stream()
            items = [{"id": d.id, **d.to_dict()} for d in docs]
        return items
    except Exception as e:
        print(f"[FirebaseAuth] Fetch todos failed: {e}")
        return []


def add_todo(text: str) -> dict | None:
    """Adds a new to-do item for the logged-in user."""
    if not _current_user or not _init_firestore() or not text.strip():
        return None
    try:
        uid = _current_user["uid"]
        ref = _db.collection("users").document(uid).collection("todos").document()
        data = {
            "text": text,
            "completed": False,
            "created_at": firestore.SERVER_TIMESTAMP
        }
        ref.set(data)
        # return matching dict
        return {"id": ref.id, "text": text, "completed": False}
    except Exception as e:
        print(f"[FirebaseAuth] Add todo failed: {e}")
        return None


def update_todo_completed(todo_id: str, completed: bool) -> bool:
    """Updates the completion status of a to-do item."""
    if not _current_user or not _init_firestore():
        return False
    try:
        uid = _current_user["uid"]
        _db.collection("users").document(uid).collection("todos").document(todo_id).update({
            "completed": completed
        })
        return True
    except Exception as e:
        print(f"[FirebaseAuth] Update todo failed: {e}")
        return False


def delete_todo(todo_id: str) -> bool:
    """Deletes a to-do item. Skips if temp (not yet persisted)."""
    if not _current_user or not _init_firestore():
        return False
    if not todo_id or todo_id == "temp":
        return False  # optimistic-only item not yet in Firestore
    try:
        uid = _current_user["uid"]
        _db.collection("users").document(uid).collection("todos").document(todo_id).delete()
        return True
    except Exception as e:
        print(f"[FirebaseAuth] Delete todo failed: {e}")
        return False


def get_spotify_playlist() -> str:
    """Fetches custom Spotify playlist URL from user settings."""
    if not _current_user or not _init_firestore():
        return ""
    try:
        uid = _current_user["uid"]
        doc = _db.collection("users").document(uid).collection("settings").document("spotify").get()
        if doc.exists:
            return doc.to_dict().get("playlist_url", "")
    except Exception as e:
        print(f"[FirebaseAuth] Fetch spotify playlist failed: {e}")
    return ""


def save_spotify_playlist(url: str) -> bool:
    """Saves custom Spotify playlist URL to user settings."""
    if not _current_user or not _init_firestore():
        return False
    try:
        uid = _current_user["uid"]
        _db.collection("users").document(uid).collection("settings").document("spotify").set({
            "playlist_url": url
        }, merge=True)
        return True
    except Exception as e:
        print(f"[FirebaseAuth] Save spotify playlist failed: {e}")
        return False


def _upsert_user():
    """Create or update the users/{uid} document in Firestore."""
    if not _current_user or not _init_firestore():
        return
    def _write():
        try:
            uid = _current_user["uid"]
            ref = _db.collection("users").document(uid)
            doc = ref.get()
            if doc.exists:
                ref.update({
                    "last_login": firestore.SERVER_TIMESTAMP,
                    "name":       _current_user.get("name"),
                    "email":      _current_user.get("email"),
                })
            else:
                ref.set({
                    "uid":         uid,
                    "name":        _current_user.get("name"),
                    "email":       _current_user.get("email"),
                    "photo_url":   _current_user.get("photo_url"),
                    "role":        "developer",
                    "first_login": firestore.SERVER_TIMESTAMP,
                    "last_login":  firestore.SERVER_TIMESTAMP,
                })
        except Exception as e:
            print(f"[FirebaseAuth] User upsert failed: {e}")
    threading.Thread(target=_write, daemon=True).start()


# ── Quick test ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import time
    print("=" * 50)
    print("FocusFox — Firebase Auth Test")
    print("=" * 50)
    print("Opening browser for Google Sign-In...")
    user = login()
    if user:
        print(f"\n✅ Logged in as: {user['name']} ({user['email']})")
        print(f"   UID: {user['uid']}")
        print("\nLogging test activity to Firestore...")
        log_action("TEST_LOGIN", details={"source": "firebase_auth.py direct test"})
        time.sleep(2)   # give background thread time to write
        print("✅ Done — check Firestore → activity_logs")
    else:
        print("❌ Login failed or was cancelled.")
