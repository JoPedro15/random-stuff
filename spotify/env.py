import os

from dotenv import load_dotenv


def load_env():
    load_dotenv()


def require(*keys: str) -> None:
    missing = [k for k in keys if not os.getenv(k)]
    if missing:
        raise SystemExit(f"Missing env vars: {', '.join(missing)}")
