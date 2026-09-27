"""Attack firestore.rules with forged identities in the local emulator (never touches the real project).

Needs Java 21+ and firebase-tools. From the repo root:
    firebase emulators:exec --only firestore --project demo-rules "python tests/test_firestore_rules.py"
"""
import base64, json, os, sys, time
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from webui.firebase import _to_rest_doc

P = "demo-rules"
BASE = f"http://127.0.0.1:8080/v1/projects/{P}/databases/(default)/documents"
fails = 0


def tok(uid, email, verified=True):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    now = int(time.time())
    return enc({"alg": "none", "typ": "JWT"}) + "." + enc({
        "sub": uid, "user_id": uid, "email": email, "email_verified": verified,
        "iss": f"https://securetoken.google.com/{P}", "aud": P, "iat": now, "exp": now + 3600,
        "auth_time": now, "firebase": {"sign_in_provider": "google.com"}}) + "."


def H(t): return {"Authorization": f"Bearer {t}"}


def expect(label, resp, ok):
    global fails
    good = (resp.status_code == 200) == ok
    fails += not good
    print(f"{'PASS' if good else 'FAIL'}  {'allow' if ok else 'deny '}  {label}  (HTTP {resp.status_code})")


A = tok("alice", "alice@x.com")
B = tok("bob", "bob@x.com")
ADM = tok("adm", "otherp1234@gmail.com")
FAKE_ADM = tok("fake", "otherp1234@gmail.com", verified=False)
req = lambda uid, email, status="pending", **kw: _to_rest_doc(
    {"uid": uid, "email": email, "name": "n", "note": "hi", "status": status, "requested_at": "t", **kw})
post = lambda t, uid, body: requests.post(f"{BASE}/dashboard_access", params={"documentId": uid}, json=body, headers=H(t))
patch = lambda t, uid, data: requests.patch(f"{BASE}/dashboard_access/{uid}",
                                            params=[("updateMask.fieldPaths", k) for k in data],
                                            json=_to_rest_doc(data), headers=H(t))
query = lambda t, coll, where=None: requests.post(f"{BASE}:runQuery", headers=H(t), json={"structuredQuery": {
    "from": [{"collectionId": coll}], **({"where": where} if where else {})}})

print("── access requests ──")
expect("alice files request pre-approved", post(A, "alice", req("alice", "alice@x.com", "approved")), False)
expect("alice files request for bob's uid", post(A, "bob", req("bob", "bob@x.com")), False)
expect("alice files request with spoofed email", post(A, "alice", req("alice", "otherp1234@gmail.com")), False)
expect("alice sneaks extra field decided_by", post(A, "alice", req("alice", "alice@x.com", decided_by="me")), False)
expect("alice note > 500 chars", post(A, "alice", req("alice", "alice@x.com", note="x" * 501)), False)
expect("alice files a proper pending request", post(A, "alice", req("alice", "alice@x.com")), True)
expect("alice approves herself", patch(A, "alice", {"status": "approved"}), False)
expect("alice deletes & re-creates (delete)", requests.delete(f"{BASE}/dashboard_access/alice", headers=H(A)), False)
expect("alice reads her own request", requests.get(f"{BASE}/dashboard_access/alice", headers=H(A)), True)
expect("bob reads alice's request", requests.get(f"{BASE}/dashboard_access/alice", headers=H(B)), False)
expect("bob lists all requests", query(B, "dashboard_access"), False)
expect("unverified 'admin' lists requests", query(FAKE_ADM, "dashboard_access"), False)
expect("unverified 'admin' approves alice", patch(FAKE_ADM, "alice", {"status": "approved"}), False)
expect("admin lists requests", query(ADM, "dashboard_access"), True)
expect("admin sets bogus status", patch(ADM, "alice", {"status": "superuser"}), False)
expect("admin rewrites alice's email", patch(ADM, "alice", {"status": "approved", "email": "evil@x.com"}), False)
expect("admin approves alice", patch(ADM, "alice", {"status": "approved", "decided_by": "otherp1234@gmail.com"}), True)
expect("admin deletes alice's request", requests.delete(f"{BASE}/dashboard_access/alice", headers=H(ADM)), True)
expect("no token at all creates request", requests.post(f"{BASE}/dashboard_access", params={"documentId": "x"},
                                                         json=req("x", "x@x.com")), False)

print("── todos ──")
todo = lambda uid: _to_rest_doc({"user_id": uid, "text": "t", "completed": False, "created_at": "c"})
expect("alice creates own todo", requests.post(f"{BASE}/todos", params={"documentId": "t1"}, json=todo("alice"), headers=H(A)), True)
expect("alice creates todo as bob", requests.post(f"{BASE}/todos", params={"documentId": "t2"}, json=todo("bob"), headers=H(A)), False)
mine = {"fieldFilter": {"field": {"fieldPath": "user_id"}, "op": "EQUAL", "value": {"stringValue": "alice"}}}
expect("alice queries her todos (web app query)", query(A, "todos", mine), True)
expect("bob queries alice's todos", query(B, "todos", mine), False)
expect("bob lists all todos", query(B, "todos"), False)
expect("bob reads alice's todo", requests.get(f"{BASE}/todos/t1", headers=H(B)), False)
expect("bob deletes alice's todo", requests.delete(f"{BASE}/todos/t1", headers=H(B)), False)
expect("alice ticks her todo", requests.patch(f"{BASE}/todos/t1", params={"updateMask.fieldPaths": "completed"},
                                              json={"fields": {"completed": {"booleanValue": True}}}, headers=H(A)), True)
expect("alice hands her todo to bob", requests.patch(f"{BASE}/todos/t1", params={"updateMask.fieldPaths": "user_id"},
                                                     json={"fields": {"user_id": {"stringValue": "bob"}}}, headers=H(A)), False)

print("── existing collections ──")
expect("anyone reads info_guides", requests.get(f"{BASE}/info_guides/nope"), False)  # 404 = allowed but missing
expect("bob writes alice's spotify", requests.patch(f"{BASE}/spotify_settings/alice", json=todo("bob"), headers=H(B)), False)
expect("bob reads activity_logs", query(B, "activity_logs"), False)
print(f"\n{'ALL RULES TESTS PASSED' if not fails else f'{fails} RULES TEST(S) FAILED'}")
sys.exit(1 if fails else 0)
