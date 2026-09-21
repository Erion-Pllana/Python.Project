"""
frontend/state.py

Centralized Streamlit session-state helpers.
"""

from typing import Optional

import streamlit as st

_TOKEN_KEY = "auth_token"
_USER_KEY = "auth_user"


def init_session_state() -> None:
    if _TOKEN_KEY not in st.session_state:
        st.session_state[_TOKEN_KEY] = None
    if _USER_KEY not in st.session_state:
        st.session_state[_USER_KEY] = None


def log_in(token: str, user: dict) -> None:
    st.session_state[_TOKEN_KEY] = token
    st.session_state[_USER_KEY] = user


def log_out() -> None:
    st.session_state[_TOKEN_KEY] = None
    st.session_state[_USER_KEY] = None


def get_token() -> Optional[str]:
    return st.session_state.get(_TOKEN_KEY)


def get_current_user() -> Optional[dict]:
    return st.session_state.get(_USER_KEY)


def is_authenticated() -> bool:
    return get_token() is not None and get_current_user() is not None


def get_role() -> Optional[str]:
    user = get_current_user()
    return user["role"] if user else None