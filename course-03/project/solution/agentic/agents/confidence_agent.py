from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

class ConfidenceScore(BaseModel):
    """Score the confidence of the resolution."""
    confidence: float = Field(..., description="A confidence score from 0 to 1 indicating how confident the system is in the resolution")
    should_escalate: bool = Field(..., description="True if the issue should be escalated to human support")
    reasoning: str = Field(..., description="Brief explanation of the confidence score")

def get_confidence_agent():
    logger.info("Initializing confidence scoring agent")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a confidence scoring agent. Your job is to evaluate the confidence level of a resolution and determine if it should be escalated to human support. "
                "A confidence score of 0.8 or higher means the resolution is reliable. Below 0.8, escalate to human support.",
            ),
            ("user", "Ticket: {ticket_text}\n\nProposed Resolution: {resolution}\n\nScoring:"),
        ]
    )
    llm = ChatOpenAI(
        model="gpt-4-turbo-preview",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )
    return prompt | llm.with_structured_output(ConfidenceScore, method='function_calling')

