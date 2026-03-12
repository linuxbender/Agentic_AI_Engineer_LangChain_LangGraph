from typing import TypedDict, Annotated, Sequence
import operator
import logging
from langchain_core.messages import BaseMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from agentic.agents.triage_agent import get_triage_agent
from agentic.agents.resolver_agent import get_resolver_agent
from agentic.agents.escalation_agent import get_escalation_agent
from agentic.agents.confidence_agent import get_confidence_agent
from agentic.logging_config import configure_structured_logging, get_structured_logger

# Configure structured logging
configure_structured_logging()
logger = get_structured_logger(__name__)

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next: str
    thread_id: str

# Get the agents
triage_agent = get_triage_agent()
resolver_agent = get_resolver_agent()
escalation_agent = get_escalation_agent()
confidence_agent = get_confidence_agent()

# Define the nodes
def triage_node(state):
    thread_id = state.get("thread_id", "unknown")
    ticket_text = state["messages"][-1].content
    
    logger.info(
        "Triage classification started",
        thread_id=thread_id,
        node_name="triage",
        agent_name="TriageAgent"
    )
    
    try:
        response = triage_agent.invoke({"ticket_text": ticket_text})
        
        logger.info(
            "Triage classification completed",
            thread_id=thread_id,
            node_name="triage",
            agent_name="TriageAgent",
            routing_decision=response.category,
            ticket_preview=ticket_text[:100]
        )
        
        return {"next": response.category, "thread_id": thread_id}
    except Exception as e:
        logger.error(
            "Triage classification failed",
            thread_id=thread_id,
            node_name="triage",
            agent_name="TriageAgent",
            error_details=str(e)
        )
        raise

def resolver_node(state):
    thread_id = state.get("thread_id", "unknown")
    ticket_text = state["messages"][-1].content
    
    logger.info(
        "Issue resolution started",
        thread_id=thread_id,
        node_name="resolver",
        agent_name="ResolverAgent",
        ticket_preview=ticket_text[:100]
    )
    
    try:
        response = resolver_agent.invoke({"messages": [state["messages"][-1]]})
        last_message = response["messages"][-1]
        
        logger.info(
            "Issue resolution completed",
            thread_id=thread_id,
            node_name="resolver",
            agent_name="ResolverAgent",
            tool_used="KnowledgeBase",
            resolution_preview=last_message.content[:100]
        )
        
        return {"messages": [last_message], "thread_id": thread_id}
    except Exception as e:
        logger.error(
            "Issue resolution failed",
            thread_id=thread_id,
            node_name="resolver",
            agent_name="ResolverAgent",
            error_details=str(e)
        )
        raise

def confidence_node(state):
    thread_id = state.get("thread_id", "unknown")
    ticket_text = state["messages"][0].content if state["messages"] else ""
    resolution_text = state["messages"][-1].content if state["messages"] else ""
    
    logger.info(
        "Confidence evaluation started",
        thread_id=thread_id,
        node_name="confidence",
        agent_name="ConfidenceAgent"
    )
    
    try:
        confidence_response = confidence_agent.invoke({
            "ticket_text": ticket_text,
            "resolution": resolution_text
        })
        
        should_escalate = confidence_response.should_escalate or confidence_response.confidence < 0.8
        next_node = "escalation" if should_escalate else "end"
        
        logger.info(
            "Confidence evaluation completed",
            thread_id=thread_id,
            node_name="confidence",
            agent_name="ConfidenceAgent",
            confidence_score=confidence_response.confidence,
            should_escalate=should_escalate,
            routing_decision=next_node,
            reasoning=confidence_response.reasoning
        )
        
        return {"next": next_node, "thread_id": thread_id}
    except Exception as e:
        logger.error(
            "Confidence evaluation failed",
            thread_id=thread_id,
            node_name="confidence",
            agent_name="ConfidenceAgent",
            error_details=str(e)
        )
        raise

def escalation_node(state):
    thread_id = state.get("thread_id", "unknown")
    history = "\n".join([msg.content for msg in state["messages"]])
    ticket_text = state["messages"][-1].content
    
    logger.info(
        "Escalation to human support initiated",
        thread_id=thread_id,
        node_name="escalation",
        agent_name="EscalationAgent",
        ticket_preview=ticket_text[:100],
        conversation_length=len(state["messages"])
    )
    
    try:
        response = escalation_agent.invoke({"ticket_text": ticket_text, "history": history})
        
        logger.info(
            "Escalation summary generated",
            thread_id=thread_id,
            node_name="escalation",
            agent_name="EscalationAgent",
            summary_preview=response.content[:100]
        )
        
        return {"messages": [AIMessage(content=response.content)], "thread_id": thread_id}
    except Exception as e:
        logger.error(
            "Escalation processing failed",
            thread_id=thread_id,
            node_name="escalation",
            agent_name="EscalationAgent",
            error_details=str(e)
        )
        raise

# Define the graph
workflow = StateGraph(AgentState)
workflow.add_node("triage", triage_node)
workflow.add_node("resolver", resolver_node)
workflow.add_node("confidence", confidence_node)
workflow.add_node("escalation", escalation_node)

# Define the edges
workflow.set_entry_point("triage")
workflow.add_conditional_edges(
    "triage",
    lambda x: x["next"],
    {
        "General Inquiry": "resolver",
        "Complex Issue": "resolver",
        "Technical Support": "resolver",
        "Complaint": "escalation",
    },
)
workflow.add_edge("resolver", "confidence")
workflow.add_conditional_edges(
    "confidence",
    lambda x: x["next"],
    {
        "end": END,
        "escalation": "escalation",
    },
)
workflow.add_edge("escalation", END)

# Compile the graph with checkpointer for session persistence
checkpointer = MemorySaver()
orchestrator = workflow.compile(checkpointer=checkpointer)
logger.info("Workflow compiled with MemorySaver checkpointer for session persistence")
