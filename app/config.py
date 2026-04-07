import os
from pathlib import Path

import oracledb
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(ENV_PATH)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

ORACLE_USER = os.getenv("ORACLE_USER")
ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD")
ORACLE_HOST = os.getenv("ORACLE_HOST")
ORACLE_PORT = int(os.getenv("ORACLE_PORT", "1521"))
ORACLE_SID = os.getenv("ORACLE_SID")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY missing in app/.env")

if not ORACLE_USER:
    raise ValueError("ORACLE_USER missing in app/.env")

if not ORACLE_PASSWORD:
    raise ValueError("ORACLE_PASSWORD missing in app/.env")

if not ORACLE_HOST:
    raise ValueError("ORACLE_HOST missing in app/.env")

if not ORACLE_SID:
    raise ValueError("ORACLE_SID missing in app/.env")


def get_oracle_dsn() -> str:
    return oracledb.makedsn(host=ORACLE_HOST, port=ORACLE_PORT, sid=ORACLE_SID)
