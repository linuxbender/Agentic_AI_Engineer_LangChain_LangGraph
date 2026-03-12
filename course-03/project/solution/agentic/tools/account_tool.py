import sqlite3
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def get_db_connection():
    # Get path relative to this file
    current_dir = Path(__file__).parent.parent.parent
    db_path = current_dir / 'data' / 'core' / 'udahub.db'
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn

def account_tool(user_id: str):
    """Retrieves account information for a given user ID."""
    logger.info(f"Account Tool: Looking up user {user_id}")
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
    conn.close()
    if user:
        result = dict(user)
        logger.info(f"Account Tool: User {user_id} found - {result}")
        return result
    logger.warning(f"Account Tool: User {user_id} not found in database")
    return {"error": "User not found"}

