from langchain_groq import ChatGroq
from ai import config

_llm = None


def get_llm() -> ChatGroq:
    global _llm
    if _llm is None:
        if not config.GROQ_API_KEY:
            raise RuntimeError("GROQ_API_KEY missing in .env")
        _llm = ChatGroq(api_key=config.GROQ_API_KEY, model=config.GROQ_MODEL,
                        temperature=config.LLM_TEMPERATURE)
    return _llm
