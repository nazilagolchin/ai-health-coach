import sqlite3
import json
from pathlib import Path
from typing import Optional
from models.user_profile import UserProfile

DB_PATH = Path("data/user.db")


def _get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def _init_db(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            id      INTEGER PRIMARY KEY,
            data    TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()


def save_profile(profile: UserProfile) -> None:
    with _get_connection() as conn:
        _init_db(conn)
        payload = json.dumps(profile.to_dict())
        conn.execute("DELETE FROM user_profile")
        conn.execute("INSERT INTO user_profile (data) VALUES (?)", (payload,))
        conn.commit()


def load_profile() -> Optional[UserProfile]:
    with _get_connection() as conn:
        _init_db(conn)
        row = conn.execute(
            "SELECT data FROM user_profile ORDER BY id DESC LIMIT 1"
        ).fetchone()
    if row is None:
        return None
    return UserProfile.from_dict(json.loads(row[0]))


def clear_profile() -> None:
    with _get_connection() as conn:
        _init_db(conn)
        conn.execute("DELETE FROM user_profile")
        conn.commit()
