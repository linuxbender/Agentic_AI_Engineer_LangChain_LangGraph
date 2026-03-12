# Agentic System Design - UDA-Hub

This document outlines the design of the UDA-Hub, a Universal Decision Agent for customer support automation.

## Architecture Pattern: Hierarchical Routing with Confidence Validation

The system uses a hierarchical multi-agent architecture with 4 specialized agents and intelligent routing based on ticket classification and confidence scoring.

### System Diagram

```
                        Customer Ticket Input
                                |
                                v
                        ┌──────────────────┐
                        │  TRIAGE AGENT    │
                        │  (Classifier)    │
                        └────────┬─────────┘
                                 |
                    ┌────────────┼────────────┐
                    |            |            |
           General/Complex    Complaint      |
                    |            |            |
                    v            v            |
                ┌────────┐   ┌──────────────┐ |
                │RESOLVER│   │ ESCALATION   │ |
                │ AGENT  │   │ AGENT        │ |
                │(Tools) │   │(Complaints)  │ |
                └────┬───┘   └────────┬─────┘ |
                     |                |       |
                     v                |       |
            ┌──────────────────┐      |       |
            │ CONFIDENCE AGENT │      |       |
            │(Validation)      │      |       |
            └────────┬─────────┘      |       |
                     |                |       |
            ┌────────┴────────┐       |       |
            |                 |       |       |
        High (≥0.8)       Low (<0.8) |       |
            |                 |       |       |
            v                 |       |       |
          RESOLVE             |       |       |
            |                 v       v       v
            |            ┌──────────────────┐
            |            │ ESCALATION AGENT │
            |            │(Human Handoff)   │
            |            └────────┬─────────┘
            |                     |
            └─────────┬───────────┘
                      |
                      v
              Final Response Output
```

## Agent Responsibilities

### 1. **Triage Agent** (Classifier)
- **Input**: Raw customer support ticket text
- **Function**: Initial classification and routing
- **Output**: Category classification (General Inquiry | Complex Issue | Complaint)
- **Logic**: Uses zero-shot classification with structured output
- **Routing Decision**:
  - General Inquiry → Resolver Agent
  - Complex Issue → Resolver Agent  
  - Complaint → Escalation Agent (direct escalation)

### 2. **Resolver Agent** (Resolution Specialist)
- **Input**: Classified ticket (General Inquiry or Complex Issue)
- **Function**: Attempt automated resolution using available tools
- **Tools Available**:
  - Knowledge Base Tool: RAG-based article retrieval
  - Account Tool: Customer account information lookup
  - Refund Tool: Refund processing
- **Output**: Resolution response or indication of failure
- **Logic**: ReAct (Reasoning + Acting) pattern for autonomous tool selection

### 3. **Confidence Agent** (Quality Validator)
- **Input**: Original ticket + proposed resolution
- **Function**: Validate resolution quality and determine escalation need
- **Output**: Confidence score (0.0-1.0), escalation boolean, reasoning
- **Decision Threshold**:
  - Score ≥ 0.8 → Accept resolution (END)
  - Score < 0.8 → Escalate to human (→ ESCALATION AGENT)
- **Logic**: Uses LLM-based evaluation against confidence criteria

### 4. **Escalation Agent** (Human Handoff Specialist)
- **Input**: Ticket + full conversation history
- **Function**: Prepare comprehensive escalation summary
- **Output**: Escalation summary with context for human agent
- **Usage**: Receives tickets that:
  - Are classified as Complaints
  - Fail Resolver resolution
  - Score below confidence threshold

## Data & Tools

### Knowledge Base
- **Source**: `data/external/cultpass_articles.jsonl` (48 articles)
- **Retrieval**: ChromaDB vector store with OpenAI embeddings
- **Coverage**: Account, billing, technical, policy, and experience topics

### Database Tools
- **Account Tool**: Query customer User data from SQLite
- **Refund Tool**: Update Ticket RefundAmount in SQLite
- **Database**: `data/core/udahub.db`

### Memory Management
- **Short-term**: Agent messages accumulated in session state
- **Long-term**: Knowledge base + customer database records
- **Session Scope**: thread_id-based conversation history

## Workflow

1.  A new customer ticket is received.
2.  The **Supervisor Agent** receives the ticket and passes it to the **Triage Agent**.
3.  The **Triage Agent** classifies the ticket and adds metadata (category, priority).
4.  The **Supervisor Agent** receives the classified ticket and routes it to the **Resolver Agent** or the **Escalation Agent**.
5.  The **Resolver Agent** uses its tools to find a solution.
    *   It may search the **Knowledge Base** for information.
    *   It may use the **Account Tool** to get customer details.
    *   It may use the **Refund Tool** to process a refund.
6.  If the **Resolver Agent** finds a solution, it generates a response and sends it back to the Supervisor.
7.  If the **Resolver Agent** cannot resolve the issue, it escalates the ticket to the **Escalation Agent**.
8.  The **Escalation Agent** creates a summary of the ticket and the steps taken so far, and flags it for human intervention.
9.  The **Supervisor Agent** sends the final response (either from the Resolver or the Escalation Agent) to the customer.

## Memory

*   **Short-Term Memory**: The conversation history for the current session will be maintained using the `thread_id`. This will allow agents to have context of the current conversation.
*   **Long-Term Memory**: Resolved issues and customer preferences will be stored in a persistent database. This will be implemented using semantic search on past resolved tickets to find similar issues and their resolutions.

