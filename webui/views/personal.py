"""Developer Tasks (Firestore to-dos) and Focus Music (Spotify) pages."""
import html
import re

import streamlit as st

from webui.firebase import FirebaseError
from webui.ui import fb, flash, log_action, page_header

CURATED = [
    ("Lofi Beats 🌸", "6zCID88oNjNv9zx6puDHKj", "Chill beats to study or relax to."),
    ("Deep Focus 🧠", "37i9dQZF1DWZeKCadgRdKQ", "Keep calm and focus with ambient sounds."),
    ("Chill Lofi Study 📚", "37i9dQZF1DX8Uebhn9wzrS", "Cozy lofi hip hop playlist."),
    ("Jazz Vibes 🎷", "37i9dQZF1DX0SM0LYsmbMT", "Relaxing jazz tunes for coding sessions."),
    ("Synthwave Chill 🌌", "37i9dQZF1DX8V4BE7YIpvE", "Retro futuristic electronic background vibes."),
    ("Peaceful Piano 🎹", "37i9dQZF1DX4sWSpwq3LiO", "Beautiful, gentle solo piano works."),
]
_PLAYLIST_ID = re.compile(r"^[A-Za-z0-9]{10,40}$")


def _need_cloud() -> bool:
    if fb():
        return True
    st.warning("☁ Firestore sync is unavailable for this session, so this page can't load your data. "
               "Sign out and sign in again; if it persists, check the FIREBASE_WEB_API_KEY secret.")
    return False


# ── Developer Tasks ───────────────────────────────────────────────────────────
def render_todo():
    page_header("📝  Developer Tasks", "todo")
    if not _need_cloud():
        return
    session = fb()
    if "todos" not in st.session_state:
        try:
            st.session_state.todos = session.get_todos()
        except FirebaseError as e:
            st.error(str(e))
            return

    with st.container(border=True):
        with st.form("todo_add", clear_on_submit=True, border=False):
            c1, c2 = st.columns([6, 1], vertical_alignment="bottom")
            text = c1.text_input("New task", placeholder="Enter new task here...", label_visibility="collapsed")
            add = c2.form_submit_button("➕ Add Task", width="stretch")
        if add and text.strip():
            try:
                st.session_state.todos.append(session.add_todo(text.strip()))
            except FirebaseError as e:
                st.error(str(e))
            else:
                log_action("ADD_TODO", content_type="todo")
                st.rerun()

        c_ref, _ = st.columns([1, 5])
        if c_ref.button("🔄 Refresh", width="stretch"):
            st.session_state.pop("todos", None)
            st.rerun()

        items = st.session_state.todos
        if not items:
            st.caption("No tasks yet — add your first one above.")
        for item in list(items):
            c1, c2, c3 = st.columns([0.5, 8, 0.7], vertical_alignment="center")
            c1.checkbox("done", value=bool(item.get("completed")), key=f"todo_chk_{item['id']}",
                        label_visibility="collapsed", on_change=_toggle, args=(item,))
            cls = "ff-done" if item.get("completed") else ""
            c2.markdown(f'<span class="{cls}">{html.escape(str(item.get("text", "")))}</span>',
                        unsafe_allow_html=True)
            if c3.button("🗑", key=f"todo_del_{item['id']}"):
                try:
                    session.delete_todo(item["id"])
                except FirebaseError as e:
                    st.error(str(e))
                else:
                    items.remove(item)
                    st.rerun()


def _toggle(item):
    new_val = bool(st.session_state.get(f"todo_chk_{item['id']}"))
    try:
        fb().update_todo_completed(item["id"], new_val)
        item["completed"] = new_val
    except FirebaseError as e:
        flash(str(e), "error")
        st.session_state[f"todo_chk_{item['id']}"] = bool(item.get("completed"))


# ── Focus Music ───────────────────────────────────────────────────────────────
def parse_playlist_id(url: str) -> str:
    url = (url or "").strip()
    pid = ""
    if "spotify:playlist:" in url:
        pid = url.split("spotify:playlist:")[-1].split("?")[0]
    elif "open.spotify.com/" in url and "/playlist/" in url:
        pid = url.split("/playlist/")[-1].split("?")[0].split("/")[0]
    return pid if _PLAYLIST_ID.match(pid) else ""


def _play_here(pid: str, content_type: str):
    st.session_state.now_playing = pid
    log_action("PLAY_MUSIC", content_type=content_type, subject=pid)


def render_spotify():
    page_header("🎵  Focus Music Player", "spotify")
    st.markdown("🎧 **Focus Sessions Spotify Player**  \nLaunch curated or custom focus playlists "
                "here, in your Spotify application, or in a new browser tab.")

    now = st.session_state.get("now_playing")
    if now and _PLAYLIST_ID.match(now):
        with st.container(border=True):
            c1, c2 = st.columns([6, 1], vertical_alignment="center")
            c1.markdown("**▶️ Now playing**")
            if c2.button("⏹ Close", width="stretch"):
                st.session_state.pop("now_playing", None)
                st.rerun()
            st.iframe(f"https://open.spotify.com/embed/playlist/{now}?utm_source=generator", height=380)

    with st.container(border=True):
        st.markdown("**🔗 Custom Spotify Playlist Link:**")
        if "spotify_url" not in st.session_state:
            saved = ""
            if fb():
                try:
                    saved = fb().get_spotify_playlist()
                except FirebaseError as e:
                    st.caption(f"Could not load your saved playlist: {e}")
            st.session_state.spotify_url = saved
        url = st.text_input("Playlist link", key="spotify_url", label_visibility="collapsed",
                            placeholder="Paste Spotify playlist link here (e.g., https://open.spotify.com/playlist/...)")
        pid = parse_playlist_id(url)
        c1, c2, c3, c4 = st.columns(4)
        if c1.button("💾 Save", width="stretch"):
            if url.strip() and not pid:
                st.error("That doesn't look like a Spotify playlist link.")
            elif not fb():
                st.error("Firestore sync is unavailable, so the link can't be saved.")
            else:
                try:
                    fb().save_spotify_playlist(url.strip())
                    st.success("Spotify playlist link saved!")
                except FirebaseError as e:
                    st.error(str(e))
        if c2.button("▶️ Play Custom", width="stretch", type="primary"):
            if not url.strip():
                st.warning("Please paste a Spotify playlist link first.")
            elif not pid:
                st.error("That doesn't look like a Spotify playlist link.")
            else:
                _play_here(pid, "spotify_custom_embed")
                st.rerun()
        if pid:
            c3.link_button("🚀 Open App", f"spotify:playlist:{pid}", width="stretch")
            c4.link_button("🌐 Open Web", f"https://open.spotify.com/playlist/{pid}", width="stretch")

    st.markdown("#### 🎵 Curated Focus Playlists:")
    cols = st.columns(2)
    for i, (title, pid, desc) in enumerate(CURATED):
        with cols[i % 2], st.container(border=True):
            st.markdown(f"**{title}**  \n<span class='ff-muted'>{desc}</span>", unsafe_allow_html=True)
            b1, b2, b3 = st.columns(3)
            b1.button("▶️ Play here", key=f"sp_play_{pid}", on_click=_play_here, args=(pid, "spotify_embed"),
                      width="stretch")
            b2.link_button("🚀 Open App", f"spotify:playlist:{pid}", width="stretch")
            b3.link_button("🌐 Open Web", f"https://open.spotify.com/playlist/{pid}", width="stretch")
