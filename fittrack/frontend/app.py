"""
frontend/app.py

Run with:
    streamlit run frontend/app.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from frontend import api_client, auth, state

st.set_page_config(page_title="FitTrack", page_icon="🏋️", layout="centered")

state.init_session_state()

st.title("FITTRACK")
st.subheader("Fitness Management System")
st.divider()

health = api_client.check_backend_health()

if health is not None and health.get("status") == "ok":
    st.caption(f"Backend Status: Connected · {health.get('application', 'FitTrack')}")
else:
    st.error("Backend Status: Not Connected")
    st.caption("Could not reach the FastAPI backend. Make sure it's running and try again.")
    if st.button("Re-check backend connection"):
        st.rerun()
    st.stop()

if not state.is_authenticated():
    login_tab, register_tab = st.tabs(["Log in", "Create account"])
    with login_tab:
        auth.render_login_form()
        st.caption(
            "Demo accounts: admin@fittrack.local · trainer@fittrack.local · "
            "member@fittrack.local (see README for the password)."
        )
    with register_tab:
        auth.render_register_form()
    st.stop()

user = state.get_current_user()
role = state.get_role()

auth.render_logout_button()
st.success(f"Logged in as **{user['username']}** ({role})")

if role == "ADMIN":
    st.header("Admin Dashboard")
    st.caption("Full admin dashboard is built out in later steps.")
elif role == "TRAINER":
    st.header("Trainer Dashboard")
    st.caption("Trainer dashboard is built out in later steps.")
else:
    st.header("Member Dashboard")
    st.caption("Member dashboard is built out in later steps.")