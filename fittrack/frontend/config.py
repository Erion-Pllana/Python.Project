"""
frontend/config.py

Configuration for the Streamlit frontend. Kept separate from
backend/config.py because the frontend and backend are two independent
processes/deployments that only talk over HTTP -- the frontend should
only ever know the backend's base URL, never its database credentials
or secret key.
"""

import os

from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
