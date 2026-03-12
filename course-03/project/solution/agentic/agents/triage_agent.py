from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
import os
import logging
from dotenv import load_dotenv
from agentic.logging_config import get_structured_logger

load_dotenv()
logger = get_structured_logger(__name__)

class Triage(BaseModel):
    """Triage the ticket to the correct department."""
    category: str = Field(..., description="The category of the ticket. One of: 'General Inquiry', 'Complex Issue', 'Technical Support', 'Complaint'")

def get_triage_agent():
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a triage agent. Your job is to classify the ticket and route it to the correct department. "
                "Categories: 'General Inquiry' for simple questions, 'Technical Support' for technical issues, 'Complex Issue' for complex problems, 'Complaint' for complaints.",
            ),
            ("user", "{ticket_text}"),
        ]
    )
    llm = ChatOpenAI(
        model="gpt-4-turbo-preview",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )
    logger.info("Triage agent initialized", agent_name="TriageAgent")
    return prompt | llm.with_structured_output(Triage, method='function_calling')
