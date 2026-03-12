"""Structured logging configuration with JSON output"""

import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict, Optional


class StructuredJSONFormatter(logging.Formatter):
    """Format logs as JSON for better searchability and parsing"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "thread_id": getattr(record, "thread_id", None),
            "agent_name": getattr(record, "agent_name", None),
            "node_name": getattr(record, "node_name", None),
            "tool_name": getattr(record, "tool_name", None),
            "routing_decision": getattr(record, "routing_decision", None),
            "confidence_score": getattr(record, "confidence_score", None),
            "should_escalate": getattr(record, "should_escalate", None),
            "tool_input": getattr(record, "tool_input", None),
            "tool_output": getattr(record, "tool_output", None),
            "error_details": getattr(record, "error_details", None),
        }
        
        # Remove None values to keep logs clean
        log_data = {k: v for k, v in log_data.items() if v is not None}
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, default=str)


class StructuredLogger:
    """Wrapper around Python logger to provide structured logging with context"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
    
    def _log_with_context(self, level: int, message: str, **context):
        """Log a message with structured context"""
        extra = {}
        for key, value in context.items():
            extra[key] = value
        self.logger.log(level, message, extra=extra)
    
    def info(self, message: str, **context):
        """Log info level with context"""
        self._log_with_context(logging.INFO, message, **context)
    
    def debug(self, message: str, **context):
        """Log debug level with context"""
        self._log_with_context(logging.DEBUG, message, **context)
    
    def warning(self, message: str, **context):
        """Log warning level with context"""
        self._log_with_context(logging.WARNING, message, **context)
    
    def error(self, message: str, **context):
        """Log error level with context"""
        self._log_with_context(logging.ERROR, message, **context)
    
    def critical(self, message: str, **context):
        """Log critical level with context"""
        self._log_with_context(logging.CRITICAL, message, **context)


def configure_structured_logging(log_level: int = logging.INFO, json_output: bool = True) -> None:
    """Configure structured logging for the entire application"""
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    
    if json_output:
        formatter = StructuredJSONFormatter()
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)


def get_structured_logger(name: str) -> StructuredLogger:
    """Get a structured logger instance"""
    return StructuredLogger(name)

