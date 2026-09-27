"""Background jobs (the web equivalent of the desktop's QThread workers).

A long import runs in a thread owned by the user's session, so clicking around the
UI (which reruns the Streamlit script) never interrupts it half-way. A fragment
polls the job and streams its log.
"""
import threading
import traceback

import streamlit as st

from webui.services import friendly_error


class Job:
    def __init__(self, fn, args):
        self.logs: list[str] = []
        self.status = "running"      # running | done | error
        self.result = ""
        self.acknowledged = False
        self._thread = threading.Thread(target=self._run, args=(fn, args), daemon=True)
        self._thread.start()

    def log(self, line: str):
        self.logs.append(line)

    def _run(self, fn, args):
        try:
            self.result = fn(self.log, *args) or "Done."
            self.status = "done"
        except Exception as e:
            self.log(f"ERROR: {friendly_error(e)}")
            print(traceback.format_exc())
            self.result = friendly_error(e)
            self.status = "error"


def _jobs() -> dict:
    return st.session_state.setdefault("_jobs", {})


def get_job(key: str) -> Job | None:
    return _jobs().get(key)


def is_running(key: str) -> bool:
    j = get_job(key)
    return bool(j and j.status == "running")


def start_job(key: str, fn, *args) -> Job | None:
    if is_running(key):
        return None
    job = Job(fn, args)
    _jobs()[key] = job
    return job


def render_job_log(key: str, title: str = "Import log", height: int = 320):
    """Live log box. Polls every second while the job runs, then reruns the page once."""
    job = get_job(key)

    @st.fragment(run_every=1.0 if job and job.status == "running" else None)
    def _box():
        j = get_job(key)
        st.markdown(f"**{title}**")
        with st.container(height=height, border=True):
            st.code("\n".join(j.logs[-800:]) if j and j.logs else "No activity yet.", language=None)
        if j and j.status != "running" and not j.acknowledged:
            j.acknowledged = True
            st.rerun(scope="app")   # re-enable buttons / show final status

    _box()
    if job and job.status == "done" and job.acknowledged:
        st.success(job.result)
    elif job and job.status == "error" and job.acknowledged:
        st.error(f"Failed: {job.result}")
