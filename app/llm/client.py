from app.config import get_settings


def create_llm():
    settings = get_settings()

    provider = settings.llm_provider.lower().strip()

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        if not settings.openai_api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        return ChatOpenAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            api_key=settings.openai_api_key,
        )

    if provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
        )

    if provider == "mock":
        return None

    raise ValueError(
        f"Unsupported LLM provider: {settings.llm_provider}. "
        "Supported providers: mock, ollama, openai."
    )