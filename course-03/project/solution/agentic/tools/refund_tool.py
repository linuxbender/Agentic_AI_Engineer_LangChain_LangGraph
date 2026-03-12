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

def refund_tool(ticket_id: int, amount: float):
    """Processes a refund for a given ticket ID and amount."""
    logger.info(
        "Refund processing initiated",
        tool_name="refund_tool",
        ticket_id=ticket_id,
        amount=amount
    )
    
    conn = get_db_connection()
    try:
        conn.execute('UPDATE Ticket SET RefundAmount = ? WHERE TicketID = ?', (amount, ticket_id))
        conn.commit()
        conn.close()
        
        logger.info(
            "Refund processed successfully",
            tool_name="refund_tool",
            ticket_id=ticket_id,
            amount=amount,
            tool_output="Refund completed"
        )
        return {"success": f"Refund of {amount} processed for ticket {ticket_id}."}
    except Exception as e:
        logger.error(
            "Refund processing failed",
            tool_name="refund_tool",
            ticket_id=ticket_id,
            amount=amount,
            error_details=str(e)
        )
        conn.close()
        return {"error": str(e)}
