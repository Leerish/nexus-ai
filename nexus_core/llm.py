from langchain_ollama import ChatOllama


def get_llm() -> ChatOllama:
    return ChatOllama(
        model="qwen3:8b",
    )
