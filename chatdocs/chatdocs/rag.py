from chatdocs.retriever import (
    Retriever
)

from chatdocs.llm import (
    LLMClient
)

from chatdocs.prompts import (
    RAG_SYSTEM_PROMPT
)

from chatdocs.memory import (
    ConversationMemory
)

from chatdocs.logger import get_logger

logger=get_logger(__name__)

class RAGEngine:

    def __init__(self):
        self.retriever=Retriever()
        self.llm=LLMClient()
        self.memory=ConversationMemory()


    def build_prompt(self,question,context,history):

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
    

    def answer(self,question):

        try:
            retrieval=self.retriever.retrieve_context(question)

            if not retrieval["found"]:

                return {
                    "answer":
                        "I don't see that "
                        "in our documents.",
                    "citations": []
                }
            
            history=self.memory.get_messages()
            
            prompt= self.build_prompt(question, retrieval["context"],history)

            messages=[
                {
                    "role": "system",
                    "content": RAG_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]

            answer=self.llm.generate(messages)

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
    

    def formate_citations(self,citations):
        if not citations:
            return ""

        lines=[]

        for source, page in citations:

            lines.append(
                f"- {source} "
                f"(p. {page})"
            )

        return "\n".join(lines)
    

    def list_sources(self):

        return self.retriever.indexer.list_sources()