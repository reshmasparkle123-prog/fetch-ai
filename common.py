"""Helpers shared by all RationSeva agents: env, agent construction, backend calls."""

import asyncio
import os

import requests
from dotenv import load_dotenv
from uagents import Agent

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "https://ration-seva.onrender.com").rstrip("/")
# Per-attempt HTTP timeout. Render's free tier can take ~50 s to wake, so a cold call
# fails at this point with retryable=True and the Coordinator retries once (warm by then).
BACKEND_TIMEOUT = float(os.getenv("BACKEND_TIMEOUT", "25"))


def env_flag(name, default=False):
    return os.getenv(name, str(default)).strip().lower() in ("1", "true", "yes", "on")


def require_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Set {name} in .env before starting (see .env.example).")
    return value


def make_agent(name, seed_env, port, mailbox_env):
    """Local endpoint by default; Agentverse mailbox when <mailbox_env>=true."""
    kwargs = dict(name=name, seed=require_env(seed_env), port=port)
    if env_flag(mailbox_env):
        kwargs["mailbox"] = True
    else:
        kwargs["endpoint"] = [f"http://127.0.0.1:{port}/submit"]
    return Agent(**kwargs)


class BackendError(Exception):
    def __init__(self, message, status=None, retryable=False):
        super().__init__(message)
        self.status = status
        self.retryable = retryable


def _post(path, data, files=None):
    try:
        r = requests.post(f"{BACKEND_URL}{path}", data=data, files=files, timeout=BACKEND_TIMEOUT)
    except (requests.Timeout, requests.ConnectionError) as e:
        raise BackendError(f"backend unreachable ({type(e).__name__}) - it may be waking up", retryable=True) from e
    if r.status_code >= 500:
        raise BackendError(f"backend error {r.status_code}", r.status_code, retryable=True)
    if r.status_code >= 400:
        try:
            detail = r.json().get("detail")
        except ValueError:
            detail = r.text[:200]
        raise BackendError(str(detail), r.status_code)
    return r.json()


async def backend_post(path, data, files=None):
    """POST form data to the RationSeva backend without blocking the agent's event loop."""
    return await asyncio.to_thread(_post, path, data, files)


async def warm_backend(logger):
    """Ping /health so a sleeping Render instance starts waking before the first real call."""
    def ping():
        return requests.get(f"{BACKEND_URL}/health", timeout=70).status_code
    try:
        logger.info(f"Backend {BACKEND_URL}/health -> {await asyncio.to_thread(ping)}")
    except requests.RequestException as e:
        logger.warning(f"Backend warm-up failed: {type(e).__name__}")
