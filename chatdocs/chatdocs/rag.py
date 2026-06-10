from chatdocs.hybrid_retriever import (
    HybridRetriever
)

from chatdocs.llm import (
    LLMClient
)

from chatdocs.reranker import (
    Reranker
)

from chatdocs.prompts import (
    RAG_SYSTEM_PROMPT
)

from chatdocs.memory import (
    ConversationMemory
)

from chatdocs.config import (
    Config
)

from chatdocs.logger import get_logger

logger = get_logger(__name__)


class RAGEngine:

    def __init__(self):
        self.retriever = HybridRetriever()
        self.llm = LLMClient()
        self.reranker = Reranker(self.llm)
        self.memory = ConversationMemory()

    def build_prompt(self, question, context, history):

        history_text = ""
        for msg in history:

            history_text += (
                f"{msg['role']}: "
                f"{msg['content']}\n"
            )

        return f"""

Conversation History:

{history_text}

Context:

{context}

Question:

{question}

Answer:
"""

    def answer(self, question):

        try:
            chunks = self.retriever.search(
                question,
                top_k=Config.RERANK_TOP_N
            )

            if Config.ENABLE_RERANK:
                reranked_chunks = self.reranker.rerank(
                    question,
                    chunks,
                    top_k=Config.FINAL_CONTEXT_K
                )
            else:
                reranked_chunks = chunks[:Config.FINAL_CONTEXT_K]

            if Config.DEBUG:
                print()
                print("After Retrieval:", len(chunks))
                print("After Rerank:", len(reranked_chunks))

            if not reranked_chunks:
                return {
                    "answer":
                        "I don't see that "
                        "in our documents.",
                    "citations": []
                }

            context = self.retriever.build_context(reranked_chunks)
            citations = self.retriever.extract_citations(reranked_chunks)

            retrieval = {
                "chunks": reranked_chunks,
                "context": context,
                "citations": citations,
                "found": self.retriever.has_results(reranked_chunks),
                "best_distance": self.retriever.best_distance(reranked_chunks)
            }

            if not retrieval["found"]:

                return {
                    "answer":
                        "I don't see that "
                        "in our documents.",
                    "citations": []
                }

            history = self.memory.get_messages()

            prompt = self.build_prompt(question, retrieval["context"], history)

            messages = [
                {
                    "role": "system",
                    "content": RAG_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]

            answer = self.llm.generate(messages)

            self.memory.add_user(question)
            self.memory.add_assistant(answer)

            return {
                "answer": answer,
                "citations":
                    retrieval["citations"]
            }

        except Exception as e:
            logger.exception("LLM call fails.")
            return {
                "answer":
                    "The assistant encountered "
                    "an error while generating "
                    "a response.",
                "citations": []
            }

    def formate_citations(self, citations):
        if not citations:
            return ""

        lines = []

        for source, page in citations:

            lines.append(
                f"- {source} "
                f"(p. {page})"
            )

        return "\n".join(lines)

    def list_sources(self):

        return self.retriever.indexer.list_sources()
