"""
firebase_auth.py — Google Auth + Firestore activity logger for FocusFox Desktop
Uses:
  - google-auth-oauthlib  → opens browser-based Google login
  - Firebase REST API     → exchanges Google ID token for Firebase identity
  - firebase-admin SDK    → writes activity logs to Firestore (bypasses security rules)
"""

import os
import sys
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

# ── Path Resolution Helpers ───────────────────────────────────────────────────
def get_resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def get_writeable_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# ── Constants ─────────────────────────────────────────────────────────────────
CREDENTIALS_PATH  = get_resource_path("credentials.json")
SERVICE_ACCT_PATH = get_resource_path("firebase_service_account.json")
TOKEN_CACHE_PATH  = get_writeable_path(".firebase_token_cache.json")

try:
    from dotenv import load_dotenv
    load_dotenv(get_resource_path(".env"))
except ImportError:
    pass

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
    """Initialize firebase-admin. Returns True on success."""
    return True


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
        id_token  = firebase_info.get("idToken", "")
    else:
        # Fallback: use Google identity directly (still unique by Google sub)
        uid       = google_info.get("id", "google_" + google_info.get("email", "unknown"))
        email     = google_info.get("email", "")
        name      = google_info.get("name", "")
        photo_url = google_info.get("picture", "")
        id_token  = google_info.get("id_token", "")

    _current_user = {
        "uid":       uid,
        "email":     email,
        "name":      name,
        "photo_url": photo_url,
        "id_token":  id_token,
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


# ── REST Firestore helper functions ───────────────────────────────────────────
import base64

def get_project_id() -> str:
    """Gets project ID dynamically from logged-in user token payload or fallback."""
    if _current_user and _current_user.get("id_token"):
        try:
            parts = _current_user["id_token"].split(".")
            if len(parts) == 3:
                payload = parts[1]
                payload += "=" * ((4 - len(payload) % 4) % 4)
                data = json.loads(base64.b64decode(payload).decode("utf-8"))
                proj = data.get("iss", "").split("/")[-1]
                if proj:
                    return proj
        except Exception as e:
            print(f"[FirebaseAuth] Parse project ID from JWT failed: {e}")
    if os.path.exists(SERVICE_ACCT_PATH):
        try:
            with open(SERVICE_ACCT_PATH, "r") as f:
                return json.load(f).get("project_id", "mvp-dashboard-c56c0")
        except Exception:
            pass
    return "mvp-dashboard-c56c0"

def _to_rest_value(val):
    if isinstance(val, bool):
        return {"booleanValue": val}
    elif isinstance(val, (int, float)):
        return {"doubleValue": float(val)}
    elif isinstance(val, dict):
        return {"mapValue": {"fields": {k: _to_rest_value(v) for k, v in val.items()}}}
    elif isinstance(val, list):
        return {"arrayValue": {"values": [_to_rest_value(v) for v in val]}}
    elif val is None:
        return {"nullValue": None}
    else:
        return {"stringValue": str(val)}

def _from_rest_value(rest_val):
    if not isinstance(rest_val, dict):
        return rest_val
    for k, v in rest_val.items():
        if k == "stringValue":
            return v
        elif k == "booleanValue":
            return bool(v)
        elif k == "doubleValue" or k == "integerValue":
            return float(v)
        elif k == "mapValue":
            return {mk: _from_rest_value(mv) for mk, mv in v.get("fields", {}).items()}
        elif k == "arrayValue":
            return [_from_rest_value(av) for av in v.get("values", [])]
        elif k == "nullValue":
            return None
    return None

def _to_rest_doc(flat_dict):
    return {"fields": {k: _to_rest_value(v) for k, v in flat_dict.items()}}

def _from_rest_doc(rest_doc):
    fields = rest_doc.get("fields", {})
    return {k: _from_rest_value(v) for k, v in fields.items()}


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
    Write an activity log record to Firestore using the REST API (non-blocking, fire-and-forget).
    Also always prints locally as a fallback.
    """
    if not _current_user or not _current_user.get("id_token"):
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

    def _write():
        try:
            pid = get_project_id()
            url = f"https://firestore.googleapis.com/v1/projects/{pid}/databases/(default)/documents/activity_logs"
            headers = {
                "Authorization": f"Bearer {_current_user['id_token']}",
                "Content-Type": "application/json"
            }
            # Append special firestore timestamp
            payload = dict(record)
            payload["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"
            doc_data = _to_rest_doc(payload)
            resp = requests.post(url, json=doc_data, headers=headers, timeout=5)
            if resp.status_code not in (200, 201):
                print(f"[ActivityLog] REST write failed: {resp.status_code} {resp.text}")
        except Exception as e:
            print(f"[ActivityLog] REST write request failed: {e}")

    threading.Thread(target=_write, daemon=True).start()


def get_guide(key: str) -> dict | None:
    """Fetches a guide document from Firestore via REST API, or returns None."""
    try:
        pid = get_project_id()
        url = f"https://firestore.googleapis.com/v1/projects/{pid}/databases/(default)/documents/info_guides/{key}"
        headers = {}
        if _current_user and _current_user.get("id_token"):
            headers["Authorization"] = f"Bearer {_current_user['id_token']}"
        elif FIREBASE_WEB_API_KEY:
            url += f"?key={FIREBASE_WEB_API_KEY}"
            
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            doc = resp.json()
            return _from_rest_doc(doc)
        else:
            print(f"[FirebaseAuth] Fetch guide failed for key '{key}'. Status: {resp.status_code}, Response: {resp.text}")
    except Exception as e:
        print(f"[FirebaseAuth] Fetch guide failed: {e}")
    return None


def get_todos() -> list:
    """Fetches the list of to-do items for the logged-in user via REST API (from flat root collection)."""
    if not _current_user or not _current_user.get("id_token"):
        return []
    try:
        uid = _current_user["uid"]
        pid = get_project_id()
        # Query only this user's docs — firestore.rules deny listing other users' to-dos
        url = f"https://firestore.googleapis.com/v1/projects/{pid}/databases/(default)/documents:runQuery"
        headers = {"Authorization": f"Bearer {_current_user['id_token']}"}
        body = {"structuredQuery": {
            "from": [{"collectionId": "todos"}],
            "where": {"fieldFilter": {"field": {"fieldPath": "user_id"}, "op": "EQUAL",
                                      "value": {"stringValue": uid}}},
        }}

        resp = requests.post(url, json=body, headers=headers, timeout=5)
        if resp.status_code == 200:
            documents = [row["document"] for row in resp.json() if row.get("document")]
            items = []
            for doc in documents:
                name = doc.get("name", "")
                todo_id = name.split("/")[-1]
                todo_data = _from_rest_doc(doc)
                if todo_data.get("user_id") == uid:
                    todo_data["id"] = todo_id
                    items.append(todo_data)
            
            # Sort locally by created_at to preserve order
            items.sort(key=lambda x: x.get("created_at") or "")
            return items
    except Exception as e:
        print(f"[FirebaseAuth] Fetch todos failed: {e}")
    return []


def add_todo(text: str) -> dict | None:
    """Adds a new to-do item for the logged-in user via REST API (to flat root collection)."""
    if not _current_user or not _current_user.get("id_token") or not text.strip():
        return None
    try:
        uid = _current_user["uid"]
        pid = get_project_id()
        url = f"https://firestore.googleapis.com/v1/projects/{pid}/databases/(default)/documents/todos"
        headers = {
            "Authorization": f"Bearer {_current_user['id_token']}",
            "Content-Type": "application/json"
        }
        data = {
            "user_id": uid,
            "text": text,
            "completed": False,
            "created_at": datetime.datetime.utcnow().isoformat() + "Z"
        }
        doc_data = _to_rest_doc(data)
        resp = requests.post(url, json=doc_data, headers=headers, timeout=5)
        if resp.status_code in (200, 201):
            doc = resp.json()
            todo_id = doc.get("name", "").split("/")[-1]
            return {"id": todo_id, "text": text, "completed": False}
    except Exception as e:
        print(f"[FirebaseAuth] Add todo failed: {e}")
    return None


def update_todo_completed(todo_id: str, completed: bool) -> bool:
    """Updates the completion status of a to-do item via REST API (in flat root collection)."""
    if not _current_user or not _current_user.get("id_token"):
        return False
    try:
        pid = get_project_id()
        url = f"https://firestore.googleapis.com/v1/projects/{pid}/databases/(default)/documents/todos/{todo_id}?updateMask.fieldPaths=completed"
        headers = {
            "Authorization": f"Bearer {_current_user['id_token']}",
            "Content-Type": "application/json"
        }
        doc_data = {
            "fields": {
                "completed": {"booleanValue": completed}
            }
        }
        resp = requests.patch(url, json=doc_data, headers=headers, timeout=5)
        return resp.status_code == 200
    except Exception as e:
        print(f"[FirebaseAuth] Update todo failed: {e}")
    return False


def delete_todo(todo_id: str) -> bool:
    """Deletes a to-do item via REST API (from flat root collection)."""
    if not _current_user or not _current_user.get("id_token"):
        return False
    if not todo_id or todo_id == "temp":
        return False
    try:
        pid = get_project_id()
        url = f"https://firestore.googleapis.com/v1/projects/{pid}/databases/(default)/documents/todos/{todo_id}"
        headers = {"Authorization": f"Bearer {_current_user['id_token']}"}
        resp = requests.delete(url, headers=headers, timeout=5)
        return resp.status_code == 200
    except Exception as e:
        print(f"[FirebaseAuth] Delete todo failed: {e}")
    return False


def get_spotify_playlist() -> str:
    """Fetches custom Spotify playlist URL from user settings via REST API (from flat root collection)."""
    if not _current_user or not _current_user.get("id_token"):
        return ""
    try:
        uid = _current_user["uid"]
        pid = get_project_id()
        url = f"https://firestore.googleapis.com/v1/projects/{pid}/databases/(default)/documents/spotify_settings/{uid}"
        headers = {"Authorization": f"Bearer {_current_user['id_token']}"}
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code == 200:
            doc = resp.json()
            todo_data = _from_rest_doc(doc)
            return todo_data.get("playlist_url", "")
    except Exception as e:
        print(f"[FirebaseAuth] Fetch spotify playlist failed: {e}")
    return ""


def save_spotify_playlist(url: str) -> bool:
    """Saves custom Spotify playlist URL to user settings via REST API (to flat root collection)."""
    if not _current_user or not _current_user.get("id_token"):
        return False
    try:
        uid = _current_user["uid"]
        pid = get_project_id()
        url_api = f"https://firestore.googleapis.com/v1/projects/{pid}/databases/(default)/documents/spotify_settings/{uid}"
        headers = {
            "Authorization": f"Bearer {_current_user['id_token']}",
            "Content-Type": "application/json"
        }
        data = {
            "user_id": uid,
            "playlist_url": url
        }
        doc_data = _to_rest_doc(data)
        resp = requests.patch(url_api, json=doc_data, headers=headers, timeout=5)
        return resp.status_code == 200
    except Exception as e:
        print(f"[FirebaseAuth] Save spotify playlist failed: {e}")
    return False


def _upsert_user():
    """Create or update the users/{uid} document in Firestore via REST API."""
    if not _current_user or not _current_user.get("id_token"):
        return
    def _write():
        try:
            uid = _current_user["uid"]
            pid = get_project_id()
            url = f"https://firestore.googleapis.com/v1/projects/{pid}/databases/(default)/documents/users/{uid}"
            headers = {
                "Authorization": f"Bearer {_current_user['id_token']}",
                "Content-Type": "application/json"
            }
            resp_get = requests.get(url, headers=headers, timeout=5)
            now_str = datetime.datetime.utcnow().isoformat() + "Z"
            if resp_get.status_code == 200:
                data = {
                    "last_login": now_str,
                    "name":       _current_user.get("name"),
                    "email":      _current_user.get("email"),
                }
                patch_url = url + "?updateMask.fieldPaths=last_login&updateMask.fieldPaths=name&updateMask.fieldPaths=email"
                requests.patch(patch_url, json=_to_rest_doc(data), headers=headers, timeout=5)
            else:
                data = {
                    "uid":         uid,
                    "name":        _current_user.get("name"),
                    "email":       _current_user.get("email"),
                    "photo_url":   _current_user.get("photo_url"),
                    "role":        "developer",
                    "first_login": now_str,
                    "last_login":  now_str,
                }
                requests.patch(url, json=_to_rest_doc(data), headers=headers, timeout=5)
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
        time.sleep(2)
        print("✅ Done — check Firestore → activity_logs")
    else:
        print("❌ Login failed or was cancelled.")
