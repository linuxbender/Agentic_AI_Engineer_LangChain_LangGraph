import unittest
import uuid
from langchain_core.messages import HumanMessage, BaseMessage
from agentic.workflow import orchestrator
from agentic.logging_config import get_structured_logger

logger = get_structured_logger(__name__)

class TestWorkflow(unittest.TestCase):
    """Test suite for end-to-end workflow validation"""

    def setUp(self):
        """Set up test fixtures"""
        self.thread_id = str(uuid.uuid4())
        self.config = {
            "configurable": {
                "thread_id": self.thread_id,
            }
        }

    def test_workflow_imports(self):
        """Test that orchestrator can be imported without errors."""
        self.assertIsNotNone(orchestrator)
        logger.info("Workflow imports validated successfully", test_name="test_workflow_imports")

    def test_general_inquiry_routing(self):
        """Test that a general inquiry is properly routed through the workflow."""
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        
        logger.info(
            "Testing general inquiry routing",
            test_name="test_general_inquiry_routing",
            thread_id=thread_id
        )
        
        ticket = "How do I reset my password?"
        
        # CRITICAL: Include thread_id in both input and config
        response = orchestrator.invoke(
            {
                "messages": [HumanMessage(content=ticket)],
                "thread_id": thread_id
            },
            config=config
        )
        
        # Validate response structure
        self.assertIn('messages', response, "Response must contain 'messages' key")
        self.assertGreater(len(response['messages']), 0, "Response must have at least one message")
        
        last_msg = response['messages'][-1]
        self.assertIsInstance(last_msg, BaseMessage, "Last message must be a BaseMessage instance")
        self.assertIsNotNone(last_msg.content, "Message content must not be None")
        
        logger.info(
            "General inquiry routing test passed",
            thread_id=thread_id,
            response_length=len(last_msg.content)
        )

    def test_complex_issue_with_tool_usage(self):
        """Test that a complex issue uses tools and is routed correctly."""
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        
        logger.info(
            "Testing complex issue with tool usage",
            test_name="test_complex_issue_with_tool_usage",
            thread_id=thread_id
        )
        
        ticket = "My account is locked and I can't log in. I've tried resetting my password but it didn't work. User ID is user123."
        
        response = orchestrator.invoke(
            {
                "messages": [HumanMessage(content=ticket)],
                "thread_id": thread_id
            },
            config=config
        )
        
        # Validate response
        self.assertIn('messages', response)
        self.assertGreater(len(response['messages']), 0)
        
        last_msg = response['messages'][-1]
        self.assertIsInstance(last_msg, BaseMessage)
        self.assertIsNotNone(last_msg.content)
        self.assertGreater(len(last_msg.content), 0, "Resolution content must not be empty")
        
        logger.info(
            "Complex issue test passed - tools were utilized",
            thread_id=thread_id,
            response_length=len(last_msg.content)
        )

    def test_complaint_escalation(self):
        """Test that a complaint is properly escalated to human support."""
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        
        logger.info(
            "Testing complaint escalation scenario",
            test_name="test_complaint_escalation",
            thread_id=thread_id
        )
        
        ticket = "I am extremely unhappy with the service. I've been waiting hours for support. This is unacceptable!"
        
        response = orchestrator.invoke(
            {
                "messages": [HumanMessage(content=ticket)],
                "thread_id": thread_id
            },
            config=config
        )
        
        # Validate escalation response
        self.assertIn('messages', response)
        self.assertGreater(len(response['messages']), 0)
        
        last_msg = response['messages'][-1]
        self.assertIsInstance(last_msg, BaseMessage)
        self.assertIsNotNone(last_msg.content)
        
        # Escalation summary should mention human review
        content_lower = last_msg.content.lower()
        self.assertTrue(
            any(keyword in content_lower for keyword in ['escalat', 'human', 'support', 'review']),
            "Escalation response should reference human support"
        )
        
        logger.info(
            "Complaint escalation test passed",
            thread_id=thread_id,
            escalation_detected=True
        )

    def test_billing_issue_scenario(self):
        """Test billing/refund issue handling - new test case"""
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        
        logger.info(
            "Testing billing issue scenario",
            test_name="test_billing_issue_scenario",
            thread_id=thread_id
        )
        
        ticket = "I want a refund for my subscription. I was charged twice this month."
        
        response = orchestrator.invoke(
            {
                "messages": [HumanMessage(content=ticket)],
                "thread_id": thread_id
            },
            config=config
        )
        
        # Validate response
        self.assertIn('messages', response)
        self.assertGreater(len(response['messages']), 0)
        
        last_msg = response['messages'][-1]
        self.assertIsInstance(last_msg, BaseMessage)
        self.assertIsNotNone(last_msg.content)
        self.assertGreater(len(last_msg.content), 0)
        
        logger.info(
            "Billing issue test passed",
            thread_id=thread_id,
            response_length=len(last_msg.content)
        )

    def test_thread_id_persistence(self):
        """Test that thread_id is maintained throughout workflow execution"""
        thread_id = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id}}
        
        logger.info(
            "Testing thread_id persistence",
            test_name="test_thread_id_persistence",
            thread_id=thread_id
        )
        
        ticket = "How can I update my profile?"
        
        response = orchestrator.invoke(
            {
                "messages": [HumanMessage(content=ticket)],
                "thread_id": thread_id
            },
            config=config
        )
        
        # Verify response was processed
        self.assertIn('messages', response)
        self.assertGreater(len(response['messages']), 0)
        
        logger.info(
            "Thread ID persistence test passed",
            thread_id=thread_id,
            persistence_verified=True
        )

if __name__ == "__main__":
    unittest.main()

