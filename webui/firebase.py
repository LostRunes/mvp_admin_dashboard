"""Per-session Firebase identity + Firestore REST helpers (web port of firebase_auth.py).

The desktop app keeps the logged-in user in a module global; on a web server that
would be shared by every visitor, so here each browser session owns its own
FirebaseSession object (stored in st.session_state).

Flow: Streamlit's Google sign-in (st.login) gives us Google's ID token → exchanged
with Firebase (signInWithIdp), exactly like the desktop → the Firebase UID is the
same one the desktop app used, so to-dos / Spotify settings carry over.
"""
import base64
import datetime
import json
import threading
import time

import requests

FIRESTORE = "https://firestore.googleapis.com/v1/projects/{pid}/databases/(default)/documents"
DEFAULT_PROJECT_ID = "mvp-dashboard-c56c0"


class FirebaseError(Exception):
    pass


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") + "Z"


def jwt_payload(token: str) -> dict:
    try:
        part = token.split(".")[1]
        part += "=" * (-len(part) % 4)
        return json.loads(base64.urlsafe_b64decode(part).decode("utf-8"))
    except Exception:
        return {}


# ── Firestore REST value conversion (identical encoding to firebase_auth.py) ──
def _to_rest_value(val):
    if isinstance(val, bool):
        return {"booleanValue": val}
    if isinstance(val, (int, float)):
        return {"doubleValue": float(val)}
    if isinstance(val, dict):
        return {"mapValue": {"fields": {k: _to_rest_value(v) for k, v in val.items()}}}
    if isinstance(val, list):
        return {"arrayValue": {"values": [_to_rest_value(v) for v in val]}}
    if val is None:
        return {"nullValue": None}
    return {"stringValue": str(val)}


def _from_rest_value(rest_val):
    if not isinstance(rest_val, dict):
        return rest_val
    for k, v in rest_val.items():
        if k in ("stringValue", "timestampValue", "referenceValue"):
            return v
        if k == "booleanValue":
            return bool(v)
        if k in ("doubleValue", "integerValue"):
            return float(v)
        if k == "mapValue":
            return {mk: _from_rest_value(mv) for mk, mv in v.get("fields", {}).items()}
        if k == "arrayValue":
            return [_from_rest_value(av) for av in v.get("values", [])]
        if k == "nullValue":
            return None
    return None


def _to_rest_doc(flat: dict) -> dict:
    return {"fields": {k: _to_rest_value(v) for k, v in flat.items()}}


def _from_rest_doc(doc: dict) -> dict:
    return {k: _from_rest_value(v) for k, v in doc.get("fields", {}).items()}


# ── Public guides (info_guides is world-readable per firestore.rules) ─────────
def fetch_guide(key: str, api_key: str | None, project_id: str) -> dict | None:
    url = f"{FIRESTORE.format(pid=project_id)}/info_guides/{key}"
    params = {"key": api_key} if api_key else None
    try:
        resp = requests.get(url, params=params, timeout=5)
        if resp.status_code == 200:
            return _from_rest_doc(resp.json())
    except requests.RequestException:
        pass
    return None


class FirebaseSession:
    """Signed-in developer: Firebase ID token (auto-refreshed) + Firestore helpers."""

    def __init__(self, api_key: str, google_id_token: str, fallback_name: str = "", fallback_email: str = ""):
        if not api_key:
            raise FirebaseError("FIREBASE_WEB_API_KEY is not configured.")
        self.api_key = api_key
        self._lock = threading.Lock()
        resp = requests.post(
            "https://identitytoolkit.googleapis.com/v1/accounts:signInWithIdp",
            params={"key": api_key},
            json={
                "requestUri": "http://localhost",
                "postBody": f"id_token={google_id_token}&providerId=google.com",
                "returnSecureToken": True,
                "returnIdpCredential": True,
            },
            timeout=10,
        )
        data = resp.json() if resp.content else {}
        if resp.status_code != 200 or "error" in data:
            msg = (data.get("error") or {}).get("message", f"HTTP {resp.status_code}")
            # Firebase echoes the raw ID token in some messages — keep only the error code.
            raise FirebaseError(f"Firebase sign-in failed: {msg.split(' :')[0].split(':')[0].strip()}")

        self.uid = data["localId"]
        self.email = data.get("email") or fallback_email
        self.name = data.get("displayName") or fallback_name
        self.photo_url = data.get("photoUrl", "")
        self._id_token = data["idToken"]
        self._refresh_token = data["refreshToken"]
        self._expires_at = time.time() + int(data.get("expiresIn", 3600))
        iss = jwt_payload(self._id_token).get("iss", "")
        self.project_id = iss.rsplit("/", 1)[-1] or DEFAULT_PROJECT_ID

    # ── token handling ────────────────────────────────────────────────────────
    def token(self) -> str:
        with self._lock:
            if time.time() > self._expires_at - 300:
                resp = requests.post(
                    "https://securetoken.googleapis.com/v1/token",
                    params={"key": self.api_key},
                    data={"grant_type": "refresh_token", "refresh_token": self._refresh_token},
                    timeout=10,
                )
                if resp.status_code != 200:
                    raise FirebaseError(f"Firebase token refresh failed (HTTP {resp.status_code})")
                d = resp.json()
                self._id_token = d["id_token"]
                self._refresh_token = d["refresh_token"]
                self._expires_at = time.time() + int(d.get("expires_in", 3600))
            return self._id_token

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token()}", "Content-Type": "application/json"}

    def _base(self) -> str:
        return FIRESTORE.format(pid=self.project_id)

    # ── activity log (fire-and-forget, like the desktop) ──────────────────────
    def log_action(self, action, content_type=None, subject=None, topic=None,
                   content_id=None, file_name=None, details=None):
        record = {
            "user_id": self.uid,
            "user_email": self.email,
            "user_name": self.name,
            "action": action,
            "content_type": content_type,
            "subject": subject,
            "topic": topic,
            "content_id": str(content_id) if content_id else None,
            "file_name": file_name,
            "details": details or {},
            "client": "web",
            "timestamp_local": _now_iso(),
        }
        print(f"[ActivityLog] {self.name} | {action} | {content_type or '-'} | {subject or '-'}")

        def _write():
            try:
                payload = dict(record, timestamp=_now_iso())
                r = requests.post(f"{self._base()}/activity_logs", json=_to_rest_doc(payload),
                                  headers=self._headers(), timeout=5)
                if r.status_code not in (200, 201):
                    print(f"[ActivityLog] write failed: {r.status_code} {r.text[:200]}")
            except Exception as e:
                print(f"[ActivityLog] write failed: {e}")

        threading.Thread(target=_write, daemon=True).start()

    def upsert_user(self):
        def _write():
            try:
                url = f"{self._base()}/users/{self.uid}"
                h = self._headers()
                now = _now_iso()
                if requests.get(url, headers=h, timeout=5).status_code == 200:
                    data = {"last_login": now, "name": self.name, "email": self.email}
                    requests.patch(url, params=[("updateMask.fieldPaths", f) for f in data],
                                   json=_to_rest_doc(data), headers=h, timeout=5)
                else:
                    data = {"uid": self.uid, "name": self.name, "email": self.email,
                            "photo_url": self.photo_url, "role": "developer",
                            "first_login": now, "last_login": now}
                    requests.patch(url, json=_to_rest_doc(data), headers=h, timeout=5)
            except Exception as e:
                print(f"[FirebaseAuth] user upsert failed: {e}")

        threading.Thread(target=_write, daemon=True).start()

    # ── to-dos (flat root collection `todos`, filtered by user_id — same data as desktop)
    def get_todos(self) -> list:
        body = {"structuredQuery": {
            "from": [{"collectionId": "todos"}],
            "where": {"fieldFilter": {"field": {"fieldPath": "user_id"}, "op": "EQUAL",
                                      "value": {"stringValue": self.uid}}},
        }}
        r = requests.post(f"{self._base()}:runQuery", json=body, headers=self._headers(), timeout=8)
        if r.status_code != 200:
            raise FirebaseError(f"Could not load tasks (HTTP {r.status_code})")
        items = []
        for row in r.json():
            doc = row.get("document")
            if not doc:
                continue
            item = _from_rest_doc(doc)
            if item.get("user_id") != self.uid:
                continue
            item["id"] = doc["name"].rsplit("/", 1)[-1]
            items.append(item)
        items.sort(key=lambda x: x.get("created_at") or "")
        return items

    def add_todo(self, text: str) -> dict:
        data = {"user_id": self.uid, "text": text, "completed": False, "created_at": _now_iso()}
        r = requests.post(f"{self._base()}/todos", json=_to_rest_doc(data), headers=self._headers(), timeout=5)
        if r.status_code not in (200, 201):
            raise FirebaseError(f"Could not add task (HTTP {r.status_code})")
        data["id"] = r.json().get("name", "").rsplit("/", 1)[-1]
        return data

    def update_todo_completed(self, todo_id: str, completed: bool):
        r = requests.patch(f"{self._base()}/todos/{todo_id}",
                           params={"updateMask.fieldPaths": "completed"},
                           json={"fields": {"completed": {"booleanValue": completed}}},
                           headers=self._headers(), timeout=5)
        if r.status_code != 200:
            raise FirebaseError(f"Could not update task (HTTP {r.status_code})")

    def delete_todo(self, todo_id: str):
        r = requests.delete(f"{self._base()}/todos/{todo_id}", headers=self._headers(), timeout=5)
        if r.status_code != 200:
            raise FirebaseError(f"Could not delete task (HTTP {r.status_code})")

    # ── Dashboard access requests (dashboard_access/{uid}) ───────────────────
    # firestore.rules: a user may only CREATE their own doc with status "pending";
    # only admins may read others, approve, reject, revoke or delete.
    def get_access_request(self) -> dict | None:
        r = requests.get(f"{self._base()}/dashboard_access/{self.uid}", headers=self._headers(), timeout=5)
        if r.status_code == 200:
            return _from_rest_doc(r.json())
        if r.status_code == 404:
            return None
        raise FirebaseError(f"Could not check your access (HTTP {r.status_code})")

    def create_access_request(self, note: str):
        data = {"uid": self.uid, "email": self.email, "name": self.name,
                "note": note[:500], "status": "pending", "requested_at": _now_iso()}
        r = requests.post(f"{self._base()}/dashboard_access", params={"documentId": self.uid},
                          json=_to_rest_doc(data), headers=self._headers(), timeout=5)
        if r.status_code not in (200, 201):
            raise FirebaseError(f"Could not send your request (HTTP {r.status_code})")

    def list_access_requests(self) -> list:
        body = {"structuredQuery": {"from": [{"collectionId": "dashboard_access"}]}}
        r = requests.post(f"{self._base()}:runQuery", json=body, headers=self._headers(), timeout=8)
        if r.status_code != 200:
            raise FirebaseError(f"Could not load access requests (HTTP {r.status_code}) — "
                                "are the latest firestore.rules deployed and your email in them?")
        out = [_from_rest_doc(row["document"]) | {"_id": row["document"]["name"].rsplit("/", 1)[-1]}
               for row in r.json() if row.get("document")]
        return sorted(out, key=lambda x: x.get("requested_at") or "", reverse=True)

    def set_access_status(self, uid: str, status: str):
        data = {"status": status, "decided_by": self.email, "decided_at": _now_iso()}
        r = requests.patch(f"{self._base()}/dashboard_access/{uid}",
                           params=[("updateMask.fieldPaths", f) for f in data] +
                                  [("currentDocument.exists", "true")],
                           json=_to_rest_doc(data), headers=self._headers(), timeout=5)
        if r.status_code != 200:
            raise FirebaseError(f"Could not update request (HTTP {r.status_code})")

    def delete_access_request(self, uid: str):
        r = requests.delete(f"{self._base()}/dashboard_access/{uid}", headers=self._headers(), timeout=5)
        if r.status_code != 200:
            raise FirebaseError(f"Could not delete request (HTTP {r.status_code})")

    # ── Spotify settings (spotify_settings/{uid}) ────────────────────────────
    def get_spotify_playlist(self) -> str:
        r = requests.get(f"{self._base()}/spotify_settings/{self.uid}", headers=self._headers(), timeout=5)
        if r.status_code == 200:
            return _from_rest_doc(r.json()).get("playlist_url", "") or ""
        if r.status_code == 404:
            return ""
        raise FirebaseError(f"Could not load playlist (HTTP {r.status_code})")

    def save_spotify_playlist(self, url: str):
        data = {"user_id": self.uid, "playlist_url": url}
        r = requests.patch(f"{self._base()}/spotify_settings/{self.uid}", json=_to_rest_doc(data),
                           headers=self._headers(), timeout=5)
        if r.status_code != 200:
            raise FirebaseError(f"Could not save playlist (HTTP {r.status_code})")
