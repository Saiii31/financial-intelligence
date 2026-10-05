"""
AI orchestrator:  question -> intent -> tools (exact data) [+ FAISS] -> context -> Groq -> answer.
Deterministic intent routing = reliable for a hackathon; the LLM only explains verified data.
"""
import re
from collections import defaultdict
from langchain_core.messages import HumanMessage, AIMessage
from ai.llm import get_llm
from ai.prompts import chat_prompt, SUMMARY_PROMPT
from ai.tools import TOOLS

# intent -> (keywords, tools to call, use_faiss)
INTENTS = {
    "monthly_expense":   (["expense last month", "spend last month", "spent last month", "monthly expense", "expense in", "expenses in"],
                          ["get_monthly_expenses", "get_cashflow"], False),
    "category_spending": (["food", "category", "where did i spend", "spend the most", "overspend", "biggest expense", "travel", "housing", "shopping"],
                          ["get_category_expenses", "get_trends"], False),
    "savings_analysis":  (["saving", "savings", "decrease", "why did", "why is", "dropped", "reduced"],
                          ["get_cashflow", "get_trends", "get_category_expenses", "get_dashboard_metrics"], False),
    "debt_priority":     (["debt", "loan", "liabilit", "interest", "emi", "credit card", "prioritize"],
                          ["get_liabilities", "get_recommendations"], False),
    "financial_health":  (["health", "score", "how am i doing", "financial position"],
                          ["get_dashboard_metrics", "get_liabilities", "get_trends", "get_recommendations"], False),
    "financial_risk":    (["risk", "problem", "worry", "concern", "danger"],
                          ["get_liabilities", "get_trends", "get_dashboard_metrics", "get_recommendations"], True),
    "income_vs_expense": (["compare", "income and expense", "income vs", "cash flow", "cashflow"],
                          ["get_cashflow", "get_trends"], False),
    "transactions":      (["transaction", "recent", "purchase", "last payment"],
                          ["get_transactions"], True),
    "next_steps":        (["what should i", "next", "recommend", "advice", "plan", "improve", "action"],
                          ["get_dashboard_metrics", "get_liabilities", "get_trends", "get_recommendations"], True),
}
GENERAL = (["get_dashboard_metrics", "get_trends"], True)

SOURCE_LABELS = {
    "get_dashboard_metrics": "dashboard", "get_cashflow": "cashflow",
    "get_monthly_expenses": "cashflow", "get_category_expenses": "expenses",
    "get_liabilities": "liabilities", "get_trends": "trends",
    "get_recommendations": "recommendations", "get_transactions": "transactions",
    "semantic_financial_search": "faiss",
}

# session_id -> list of messages, last_intent
_history = defaultdict(list)
_last_intent = {}


def detect_intent(question: str, session_id: str) -> str:
    q = question.lower()
    # short follow-ups ("why?", "and the previous month?") reuse the last intent
    if len(q.split()) <= 4 and session_id in _last_intent:
        return _last_intent[session_id]
    best, best_hits = None, 0
    for intent, (kws, _, _) in INTENTS.items():
        hits = sum(1 for k in kws if k in q)
        if hits > best_hits:
            best, best_hits = intent, hits
    return best or "general"


def _month_in(question: str) -> str:
    months = ["january", "february", "march", "april", "may", "june", "july",
              "august", "september", "october", "november", "december"]
    for m in months:
        if m in question.lower():
            return m.capitalize()
    return ""


def gather_context(intent: str, question: str):
    tool_names, use_faiss = (INTENTS[intent][1], INTENTS[intent][2]) if intent in INTENTS else GENERAL
    blocks, sources = [], []
    for name in tool_names:
        args = {}
        if name == "get_monthly_expenses":
            args = {"month": _month_in(question)}
        result = TOOLS[name].invoke(args)
        blocks.append(f"[{SOURCE_LABELS[name]}]\n{result}")
        sources.append(SOURCE_LABELS[name])
    if use_faiss:
        try:
            blocks.append(f"[context]\n{TOOLS['semantic_financial_search'].invoke({'query': question})}")
            sources.append("faiss")
        except Exception as e:  # FAISS failure must not break the chat
            print("[agent] faiss skipped:", e)
    return "\n\n".join(blocks), list(dict.fromkeys(sources))


def ask(question: str, session_id: str = "default") -> dict:
    intent = detect_intent(question, session_id)
    context, sources = gather_context(intent, question)
    chain = chat_prompt | get_llm()
    resp = chain.invoke({"context": context, "history": _history[session_id][-6:],
                         "question": question})
    answer = resp.content.strip()
    _history[session_id] += [HumanMessage(question), AIMessage(answer)]
    _last_intent[session_id] = intent
    return {"answer": answer, "sources": sources, "intent": intent}


_summary_cache = {}


def dashboard_summary(refresh: bool = False) -> dict:
    if "s" in _summary_cache and not refresh:
        return _summary_cache["s"]
    ctx, sources = gather_context("next_steps", "financial summary")
    text = (SUMMARY_PROMPT | get_llm()).invoke({"context": ctx}).content.strip()
    _summary_cache["s"] = {"summary": text, "sources": sources}
    return _summary_cache["s"]
