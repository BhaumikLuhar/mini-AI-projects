import re


class Reranker:

    def __init__(self, llm_client):
        self.llm = llm_client

    def build_prompt(self, question, chunks):

        prompt = f"""You are a retrieval reranker.

Question:

{question}

Below are candidate chunks.

Select the 5 most useful chunks for answering the question.

Return ONLY chunk numbers as a comma-separated list.

Example:

3,7,12,1,5
"""

        for idx, chunk in enumerate(chunks):
            prompt += (
                f"\n\nChunk {idx + 1}\n"
            )
            prompt += chunk["text"][:1000]

        return prompt

    def parse_response(self, response):

        if not response:
            return []

        matches = re.findall(r"\d+", response)

        return [int(match) - 1 for match in matches]

    def rerank(self, question, chunks, top_k=5):

        if not chunks:
            return []

        prompt = self.build_prompt(question, chunks)

        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]

        response = self.llm.generate(messages)
        indices = self.parse_response(response)

        ranked = []
        seen = set()

        for idx in indices:
            if idx < 0 or idx >= len(chunks):
                continue

            if idx in seen:
                continue

            ranked.append(chunks[idx])
            seen.add(idx)

            if len(ranked) >= top_k:
                break

        if not ranked:
            return chunks[:top_k]

        return ranked[:top_k]
