#!/usr/bin/env python
"""Test script for UDA-Hub Agentic App"""

import sys
import os
from pathlib import Path

# Add the solution directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agentic.workflow import orchestrator
from langchain_core.messages import HumanMessage

def test_workflow():
    """Test the workflow with various ticket types"""
    
    test_tickets = [
        "I need help with my account information",
        "I want a refund for my subscription",
        "Your service is terrible and I'm very upset",
    ]
    
    print("=" * 60)
    print("Testing UDA-Hub Agentic Workflow")
    print("=" * 60)
    
    for i, ticket in enumerate(test_tickets, 1):
        print(f"\n📋 Test {i}: {ticket}")
        print("-" * 60)
        
        try:
            # Invoke the workflow
            result = orchestrator.invoke({"messages": [HumanMessage(content=ticket)]})
            
            # Get the final message from the workflow
            final_message = result['messages'][-1]
            print(f"✅ Response: {final_message.content}")
            
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)

if __name__ == "__main__":
    test_workflow()

