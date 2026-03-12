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

def refund_tool(ticket_id: int, amount: float):
    """Processes a refund for a given ticket ID and amount."""
    logger.info(f"Refund Tool: Processing refund of ${amount} for ticket {ticket_id}")
    conn = get_db_connection()
    try:
        conn.execute('UPDATE Ticket SET RefundAmount = ? WHERE TicketID = ?', (amount, ticket_id))
        conn.commit()
        conn.close()
        logger.info(f"Refund Tool: Refund of ${amount} successfully processed for ticket {ticket_id}")
        return {"success": f"Refund of {amount} processed for ticket {ticket_id}."}
    except Exception as e:
        logger.error(f"Refund Tool: Failed to process refund - {str(e)}")
        conn.close()
        return {"error": str(e)}

