"""
Semantic retrieval: financial facts -> text documents -> MiniLM embeddings -> FAISS.
Index is persisted on disk and only rebuilt when missing (or build_index(force=True)).
"""
import os
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from ai import config
from ai.data_client import fetch

_embeddings = None
_store = None


def _emb():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name=config.EMBED_MODEL)
    return _embeddings


def build_documents() -> list[Document]:
    docs = []
    for l in fetch("/api/liabilities") or []:
        docs.append(Document(page_content=(
            f"Liability: {l['type']}. Outstanding ₹{l['outstanding']:,}. "
            f"Interest rate {l['interest_rate']}%. Monthly EMI ₹{l['emi']:,}."),
            metadata={"source": "liabilities"}))
    for e in fetch("/api/expenses") or []:
        docs.append(Document(page_content=(
            f"Spending category {e['category']}: ₹{e['amount']:,}, "
            f"{e['percentage']}% of total expenses."), metadata={"source": "expenses"}))
    for c in fetch("/api/cashflow") or []:
        docs.append(Document(page_content=(
            f"Cash flow {c['month']}: income ₹{c['income']:,}, expenses ₹{c['expenses']:,}, "
            f"savings ₹{c['savings']:,}."), metadata={"source": "cashflow"}))
    t = fetch("/api/trends")
    if t:
        top = t.get("top_spending_increase") or {}
        docs.append(Document(page_content=(
            f"Trend vs previous month: income {t['income_change']}%, expenses {t['expense_change']}%, "
            f"savings {t['savings_change']}%. Biggest spending increase: "
            f"{top.get('category')} {top.get('change')}%."), metadata={"source": "trends"}))
    for r in fetch("/api/recommendations") or []:
        docs.append(Document(page_content=(
            f"Recommendation ({r['priority']}, {r['category']}): {r['recommendation']}"),
            metadata={"source": "recommendations"}))
    for tx in (fetch("/api/transactions") or [])[:300]:  # cap for speed
        docs.append(Document(page_content=(
            f"Transaction on {tx['date']}: {tx['type']} of ₹{tx['amount']:,} in {tx['category']} "
            f"({tx['description']})."), metadata={"source": "transactions"}))
    return docs


def build_index(force: bool = False):
    global _store
    if not force and os.path.exists(config.VECTORSTORE_DIR):
        _store = FAISS.load_local(config.VECTORSTORE_DIR, _emb(),
                                  allow_dangerous_deserialization=True)
        return _store
    docs = build_documents()
    if not docs:
        raise RuntimeError("No documents to index - is the data API reachable?")
    _store = FAISS.from_documents(docs, _emb())
    os.makedirs(config.VECTORSTORE_DIR, exist_ok=True)
    _store.save_local(config.VECTORSTORE_DIR)
    return _store


def search(query: str, k: int = 5) -> list[dict]:
    store = _store or build_index()
    return [{"text": d.page_content, "source": d.metadata.get("source")}
            for d in store.similarity_search(query, k=k)]
