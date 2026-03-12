# reset_udahub.py
import os
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from langchain_core.messages import (
    SystemMessage,
    HumanMessage, 
)
from langgraph.graph.state import CompiledStateGraph


Base = declarative_base()

def reset_db(db_path: str, echo: bool = True):
    """Drops the existing udahub.db file and recreates all tables."""

    # Remove the file if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✅ Removed existing {db_path}")

    # Create a new engine and recreate tables
    engine = create_engine(f"sqlite:///{db_path}", echo=echo)
    Base.metadata.create_all(engine)
    print(f"✅ Recreated {db_path} with fresh schema")


@contextmanager
def get_session(engine: Engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def model_to_dict(instance):
    """Convert a SQLAlchemy model instance to a dictionary."""
    return {
        column.name: getattr(instance, column.name)
        for column in instance.__table__.columns
    }

def chat_interface(agent:CompiledStateGraph, ticket_id:str):
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Starting chat session with thread_id: {ticket_id}")
    
    is_first_iteration = False
    messages = [SystemMessage(content = f"ThreadId: {ticket_id}")]
    while True:
        user_input = input("User: ")
        print("User:", user_input)
        if user_input.lower() in ["quit", "exit", "q"]:
            logger.info(f"Chat session ended for thread_id: {ticket_id}")
            print("Assistant: Goodbye!")
            break
        messages = [HumanMessage(content=user_input)]
        if is_first_iteration:
            messages.append(HumanMessage(content=user_input))
        trigger = {
            "messages": messages
        }
        config = {
            "configurable": {
                "thread_id": ticket_id,
            }
        }
        logger.info(f"Processing message in thread {ticket_id}: {user_input[:50]}...")
        result = agent.invoke(input=trigger, config=config)
        assistant_response = result["messages"][-1].content
        logger.info(f"Generated response: {assistant_response[:50]}...")
        print("Assistant:", assistant_response)
        is_first_iteration = False