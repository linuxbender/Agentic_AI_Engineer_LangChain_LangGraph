import sqlite3
import logging
from pathlib import Path
from agentic.logging_config import get_structured_logger

logger = get_structured_logger(__name__)

def get_db_connection():
    # Get path relative to this file
    current_dir = Path(__file__).parent.parent.parent
    db_path = current_dir / 'data' / 'core' / 'udahub.db'
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn

def account_tool(user_id: str):
    """Retrieves account information for a given user ID."""
    logger.info(
        "Account lookup initiated",
        tool_name="account_tool",
        user_id=user_id
    )
    
    try:
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchone()
        conn.close()
        
        if user:
            result = dict(user)
            logger.info(
                "Account found",
                tool_name="account_tool",
                user_id=user_id,
                tool_output="User details retrieved successfully"
            )
            return result
        
        logger.warning(
            "Account not found",
            tool_name="account_tool",
            user_id=user_id
        )
        return {"error": "User not found"}
    except Exception as e:
        logger.error(
            "Account lookup failed",
            tool_name="account_tool",
            user_id=user_id,
            error_details=str(e)
        )
        return {"error": str(e)}
