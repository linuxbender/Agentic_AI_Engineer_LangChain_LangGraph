from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from agentic.tools.kb_tool import knowledge_base_tool
from agentic.tools.account_tool import account_tool
from agentic.tools.refund_tool import refund_tool
import os
import logging
from dotenv import load_dotenv
from agentic.logging_config import get_structured_logger

load_dotenv()
logger = get_structured_logger(__name__)

def get_resolver_agent():
    logger.info("Initializing resolver agent", agent_name="ResolverAgent")
    llm = ChatOpenAI(
        model="gpt-4-turbo-preview",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL")
    )
    # Convert tools to langchain Tool format
    tools = [knowledge_base_tool, account_tool, refund_tool]
    logger.info(
        "Resolver agent configured with tools",
        agent_name="ResolverAgent",
        tools_count=len(tools),
        tools_list=["knowledge_base", "account", "refund"]
    )
    agent = create_agent(llm, tools)
    return agent

