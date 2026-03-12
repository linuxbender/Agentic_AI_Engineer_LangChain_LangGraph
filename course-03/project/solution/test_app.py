#!/usr/bin/env python
"""Test script for UDA-Hub Agentic App - End-to-End Demonstration"""

import sys
import os
import uuid
import json
from pathlib import Path

# Add the solution directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agentic.workflow import orchestrator
from agentic.logging_config import get_structured_logger
from langchain_core.messages import HumanMessage

logger = get_structured_logger(__name__)

# Test tickets covering different scenarios
TEST_TICKETS = {
    "general_inquiry": {
        "description": "General account inquiry - should resolve via KB",
        "content": "How do I reset my password for my account?"
    },
    "billing_issue": {
        "description": "Billing/refund request - tests tool usage",
        "content": "I want a refund for my subscription. I was charged twice this month."
    },
    "technical_support": {
        "description": "Technical support - complex issue requiring tools",
        "content": "I'm unable to log in. I've tried resetting my password but it still doesn't work. My account keeps showing an error."
    },
    "complaint": {
        "description": "Complaint - should escalate to human",
        "content": "Your service is absolutely terrible! I've been waiting 3 hours for help. This is completely unacceptable!"
    }
}

def run_test_scenario(ticket_key: str, ticket_data: dict) -> dict:
    """Run a single test scenario and return results"""
    thread_id = str(uuid.uuid4())
    
    logger.info(
        "Starting test scenario",
        thread_id=thread_id,
        ticket_type=ticket_key,
        description=ticket_data["description"]
    )
    
    print(f"\n{'='*80}")
    print(f"📋 Test: {ticket_key.upper()}")
    print(f"Description: {ticket_data['description']}")
    print(f"Thread ID: {thread_id}")
    print(f"-" * 80)
    print(f"Customer: {ticket_data['content']}")
    print(f"-" * 80)
    
    result = {
        "ticket_type": ticket_key,
        "thread_id": thread_id,
        "status": "FAILED",
        "error": None,
        "response": None
    }
    
    try:
        # CRITICAL: Must include thread_id in config for checkpointer
        config = {
            "configurable": {
                "thread_id": thread_id,
            }
        }
        
        # Invoke the workflow
        response = orchestrator.invoke(
            {"messages": [HumanMessage(content=ticket_data['content'])], "thread_id": thread_id},
            config=config
        )
        
        # Get the final message from the workflow
        final_message = response['messages'][-1]
        response_text = final_message.content if hasattr(final_message, 'content') else str(final_message)
        
        logger.info(
            "Test scenario completed successfully",
            thread_id=thread_id,
            ticket_type=ticket_key,
            response_length=len(response_text)
        )
        
        result["status"] = "SUCCESS"
        result["response"] = response_text
        
        print(f"✅ Assistant Response:\n{response_text}\n")
        
    except Exception as e:
        error_msg = f"{type(e).__name__}: {str(e)}"
        
        logger.error(
            "Test scenario failed with exception",
            thread_id=thread_id,
            ticket_type=ticket_key,
            error_type=type(e).__name__,
            error_details=str(e)
        )
        
        result["status"] = "FAILED"
        result["error"] = error_msg
        print(f"❌ Error: {error_msg}\n")
        import traceback
        traceback.print_exc()
    
    return result

def main():
    """Run all test scenarios"""
    print("\n" + "=" * 80)
    print("🚀 UDA-Hub Agentic Workflow - End-to-End Test Suite")
    print("=" * 80)
    
    results = []
    
    for ticket_key in ["general_inquiry", "billing_issue", "technical_support", "complaint"]:
        ticket_data = TEST_TICKETS[ticket_key]
        result = run_test_scenario(ticket_key, ticket_data)
        results.append(result)
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 Test Summary")
    print("=" * 80)
    
    success_count = sum(1 for r in results if r["status"] == "SUCCESS")
    total_count = len(results)
    
    for result in results:
        status_icon = "✅" if result["status"] == "SUCCESS" else "❌"
        print(f"{status_icon} {result['ticket_type']:20} - {result['status']:10} (Thread: {result['thread_id'][:8]}...)")
        if result["error"]:
            print(f"   Error: {result['error']}")
    
    print(f"\n📈 Results: {success_count}/{total_count} tests passed")
    print("=" * 80)
    
    # Return exit code based on results
    return 0 if success_count == total_count else 1

if __name__ == "__main__":
    sys.exit(main())

