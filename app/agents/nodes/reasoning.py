from app.agents.state import AgentState
from app.llm.reasoning import run_reasoning


def reasoning_node(state: AgentState) -> AgentState:
    """
    LangGraph reasoning node.

    Delegates incident reasoning to the configured
    LLM provider.

    Current development provider:
        mock

    Future providers:
        ollama
        openai
    """

    return run_reasoning(state)