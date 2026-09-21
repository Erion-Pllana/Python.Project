"""
frontend/api_client.py
"""

from typing import Optional

import httpx

from frontend.config import API_BASE_URL

DEFAULT_TIMEOUT = 5.0


def check_backend_health() -> Optional[dict]:
    url = f"{API_BASE_URL}/api/health"
    try:
        response = httpx.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except (httpx.RequestError, httpx.HTTPStatusError):
        return None


def register(username, email, password, first_name, last_name, phone: Optional[str] = None) -> dict:
    url = f"{API_BASE_URL}/api/auth/register"
    payload = {
        "username": username, "email": email, "password": password,
        "first_name": first_name, "last_name": last_name, "phone": phone,
    }
    response = httpx.post(url, json=payload, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response.json()


def login(username_or_email: str, password: str) -> dict:
    url = f"{API_BASE_URL}/api/auth/login"
    payload = {"username_or_email": username_or_email, "password": password}
    response = httpx.post(url, json=payload, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response.json()


def get_current_user(token: str) -> dict:
    url = f"{API_BASE_URL}/api/auth/me"
    headers = {"Authorization": f"Bearer {token}"}
    response = httpx.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    return response.json()