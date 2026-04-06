from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import os


def load_dotenv_file():
    env_path = Path.cwd() / ".env"

    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()

        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue

        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


@dataclass(frozen=True)
class Settings:
    movieglu_api_base_url: str
    movieglu_client: str
    movieglu_api_key: str
    movieglu_authorization: str
    movieglu_territory: str
    movieglu_api_version: str
    movieglu_geolocation: str
    movieglu_cinema_query: str
    movieglu_cinema_name_hint: str
    movieglu_show_date: str


def require_env(name: str) -> str:
    value = os.getenv(name)

    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")

    return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    load_dotenv_file()

    return Settings(
        movieglu_api_base_url=require_env("MOVIEGLU_API_BASE_URL"),
        movieglu_client=require_env("MOVIEGLU_CLIENT"),
        movieglu_api_key=require_env("MOVIEGLU_API_KEY"),
        movieglu_authorization=require_env("MOVIEGLU_AUTHORIZATION"),
        movieglu_territory=require_env("MOVIEGLU_TERRITORY"),
        movieglu_api_version=require_env("MOVIEGLU_API_VERSION"),
        movieglu_geolocation=require_env("MOVIEGLU_GEOLOCATION"),
        movieglu_cinema_query=os.getenv("MOVIEGLU_CINEMA_QUERY", "odeon coventry"),
        movieglu_cinema_name_hint=os.getenv("MOVIEGLU_CINEMA_NAME_HINT", "ODEON Coventry"),
        movieglu_show_date=os.getenv("MOVIEGLU_SHOW_DATE", "2026-04-06"),
    )
