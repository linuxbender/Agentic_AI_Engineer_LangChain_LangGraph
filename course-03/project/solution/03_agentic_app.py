import os
import sys
import logging
import uuid
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from agentic.workflow import orchestrator

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    # Generate or use provided thread_id for session persistence
    thread_id = str(uuid.uuid4())
    logger.info(f"Starting new session with thread_id: {thread_id}")
    
    print("Welcome to UDA-Hub!")
    print("Enter 'quit' to exit.\n")
    sys.stdout.flush()

    while True:
        user_input = input("User: ").strip()
        sys.stdout.flush()
        
        # Echo the user input (in case it wasn't shown due to piped input)
        if not sys.stdin.isatty():
            sys.stdout.write(f"{user_input}\n")
            sys.stdout.flush()
        
        if user_input.lower() == "quit":
            logger.info(f"Session ended: {thread_id}")
            print("Thank you for using UDA-Hub. Goodbye!")
            sys.stdout.flush()
            break

        logger.info(f"[Thread: {thread_id}] User input: {user_input[:100]}...")
        
        # Invoke orchestrator with thread_id for checkpointed persistence
        config = {
            "configurable": {
                "thread_id": thread_id,
            }
        }
        
        response = orchestrator.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config
        )
        
        # Extract the assistant's response content
        assistant_message = response['messages'][-1]
        response_text = assistant_message.content if hasattr(assistant_message, 'content') else str(assistant_message)
        logger.info(f"[Thread: {thread_id}] Assistant response: {response_text[:100]}...")
        
        print(f"\nAssistant: {response_text}")
        print("\n" + "="*80 + "\n")
        sys.stdout.flush()

if __name__ == "__main__":
    main()

