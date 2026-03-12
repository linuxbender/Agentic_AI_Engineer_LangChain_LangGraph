import os
import sys
import logging
import uuid
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from agentic.workflow import orchestrator
from agentic.logging_config import configure_structured_logging, get_structured_logger

load_dotenv()

# Configure structured logging
configure_structured_logging()
logger = get_structured_logger(__name__)

def main():
    # Generate or use provided thread_id for session persistence
    thread_id = str(uuid.uuid4())
    logger.info(
        "Starting new UDA-Hub session",
        thread_id=thread_id,
        application="agentic_app"
    )
    
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
            logger.info(
                "Session ended by user",
                thread_id=thread_id,
                application="agentic_app"
            )
            print("Thank you for using UDA-Hub. Goodbye!")
            sys.stdout.flush()
            break

        logger.info(
            "Processing user input",
            thread_id=thread_id,
            user_input_preview=user_input[:100]
        )
        
        try:
            # CRITICAL: Must include thread_id in both input and config for checkpointer
            config = {
                "configurable": {
                    "thread_id": thread_id,
                }
            }
            
            response = orchestrator.invoke(
                {
                    "messages": [HumanMessage(content=user_input)],
                    "thread_id": thread_id
                },
                config=config
            )
            
            # Extract the assistant's response content
            assistant_message = response['messages'][-1]
            response_text = assistant_message.content if hasattr(assistant_message, 'content') else str(assistant_message)
            
            logger.info(
                "Response generated successfully",
                thread_id=thread_id,
                response_length=len(response_text)
            )
            
            print(f"\nAssistant: {response_text}")
            print("\n" + "="*80 + "\n")
            sys.stdout.flush()
            
        except Exception as e:
            logger.error(
                "Error processing user input",
                thread_id=thread_id,
                error_type=type(e).__name__,
                error_details=str(e)
            )
            print(f"\nError: {str(e)}")
            print("\n" + "="*80 + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()

