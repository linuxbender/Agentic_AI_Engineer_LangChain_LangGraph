from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os
import logging
from dotenv import load_dotenv
from agentic.logging_config import get_structured_logger

load_dotenv()
logger = get_structured_logger(__name__)

def get_escalation_agent():
    logger.info("Initializing escalation agent for human handoff", agent_name="EscalationAgent")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an escalation agent. Your job is to create a comprehensive summary of the ticket for a human agent to review and handle.",
            ),
            ("user", "Ticket Text: {ticket_text}\n\nHistory:\n{history}"),
        ]
    )
    llm = ChatOpenAI(
        model="gpt-4-turbo-preview",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )
    return prompt | llm
