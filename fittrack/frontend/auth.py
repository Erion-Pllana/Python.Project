"""
frontend/auth.py

Streamlit-side authentication UI: login form, registration form,
logout. These call FastAPI via api_client -- Streamlit never checks a
password itself.
"""

from typing import Optional

import httpx
import streamlit as st

from frontend import api_client, state


def render_login_form() -> None:

    st.subheader("Log in")

    with st.form("login_form"):

        username_or_email = st.text_input(
            "Username or email"
        )

        password = st.text_input(
            "Password",
            type="password",
        )

        submitted = st.form_submit_button(
            "Log in",
            use_container_width=True,
        )

    if not submitted:
        return

    if not username_or_email or not password:
        st.error(
            "Enter both a username/email and a password."
        )
        return

    try:

        token_data = api_client.login(
            username_or_email,
            password,
        )

        token = token_data["access_token"]

        user = api_client.get_current_user(
            token
        )

        state.log_in(
            token,
            user,
        )

        st.rerun()

    except httpx.HTTPStatusError as exc:

        st.error(
            _extract_detail(exc)
            or "Login failed. Check your credentials."
        )

    except httpx.RequestError:

        st.error(
            "Could not reach the backend. Is FastAPI running?"
        )


def render_register_form() -> None:

    st.subheader("Create a member account")

    with st.form("register_form"):

        col1, col2 = st.columns(2)

        first_name = col1.text_input(
            "First name"
        )

        last_name = col2.text_input(
            "Last name"
        )

        username = st.text_input(
            "Username"
        )

        email = st.text_input(
            "Email"
        )

        phone = st.text_input(
            "Phone (optional)"
        )

        password = st.text_input(
            "Password",
            type="password",
        )

        confirm_password = st.text_input(
            "Confirm password",
            type="password",
        )

        submitted = st.form_submit_button(
            "Create account",
            use_container_width=True,
        )

    if not submitted:
        return

    if not all(
        [
            first_name,
            last_name,
            username,
            email,
            password,
        ]
    ):
        st.error(
            "Please fill in all required fields."
        )
        return

    if password != confirm_password:
        st.error(
            "Passwords do not match."
        )
        return

    if len(password) < 8:
        st.error(
            "Password must be at least 8 characters."
        )
        return

    try:

        api_client.register(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone or None,
        )

        st.success(
            "Account created! Switch to the Log in tab to sign in."
        )

    except httpx.HTTPStatusError as exc:

        st.error(
            _extract_detail(exc)
            or "Registration failed."
        )

    except httpx.RequestError:

        st.error(
            "Could not reach the backend. Is FastAPI running?"
        )


def render_logout_button() -> None:

    if st.sidebar.button(
        "Log out",
        use_container_width=True,
    ):

        state.log_out()
        st.rerun()


def _extract_detail(
    exc: httpx.HTTPStatusError,
) -> Optional[str]:

    try:
        return exc.response.json().get(
            "detail"
        )

    except Exception:
        return None


def render_change_password_form() -> None:
    """Render a small authenticated password-change form in the sidebar."""

    token = state.get_token()

    if not token:
        return

    with st.sidebar.expander(
        "Change password"
    ):

        with st.form(
            "change_password_form"
        ):

            current = st.text_input(
                "Current password",
                type="password",
            )

            new = st.text_input(
                "New password",
                type="password",
            )

            confirm = st.text_input(
                "Confirm new password",
                type="password",
            )

            submitted = st.form_submit_button(
                "Update password",
                use_container_width=True,
            )

        if not submitted:
            return

        if not current or not new:
            st.error(
                "Enter your current and new password."
            )
            return

        if len(new) < 8:
            st.error(
                "New password must be at least 8 characters."
            )
            return

        if new != confirm:
            st.error(
                "New passwords do not match."
            )
            return

        try:

            api_client.change_password(
                token,
                current,
                new,
            )

            st.success(
                "Password updated successfully. "
                "Your current session remains active."
            )

        except httpx.HTTPStatusError as exc:

            detail = _extract_detail(exc)

            if exc.response.status_code == 401:

                state.log_out()

                st.error(
                    "Your session expired. Please log in again."
                )

                st.rerun()

            st.error(
                detail
                or "Could not update the password."
            )

        except httpx.RequestError:

            st.error(
                "Could not reach the backend. Is FastAPI running?"
            )