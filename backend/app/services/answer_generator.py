from typing import List, Dict, Any, Optional
from backend.app.config import settings
from backend.app.services.hybrid_retriever import hybrid_retriever
from backend.app.services.reranker import reranker
from backend.app.services.citation_verifier import citation_verifier
from backend.app.ai.llm_client import llm_client

class AnswerGenerator:
    """Orchestrates hybrid retrieval, cross-encoder reranking, refusal gate thresholding, mode-specific prompt formatting, LLM call, and citation verification."""

    REFUSAL_MESSAGE = (
        "I'm sorry, but the answer to this question is not available in your "
        "uploaded study materials. Please verify if you have uploaded the relevant textbook chapter or lecture notes."
    )

    MODE_INSTRUCTIONS = {
        "short": (
            "STRICT FORMATTING REQUIREMENT (SHORT MODE):\n"
            "- Provide a CONCISE, 2 to 3 sentence direct summary answer.\n"
            "- Do NOT use long bulleted lists, multiple subheadings, or unnecessary conversational filler.\n"
            "- Be precise and to the point."
        ),
        "detailed": (
            "STRICT FORMATTING REQUIREMENT (DETAILED MODE):\n"
            "- Provide a STRUCTURED, comprehensive explanation.\n"
            "- Use clear Markdown subheadings (e.g. ### Subheading), bullet points, and bold key technical terms."
        ),
        "exam": (
            "STRICT FORMATTING REQUIREMENT (EXAM-STYLE MODE):\n"
            "Format the answer specifically for University Exam Preparation into 3 distinct sections:\n"
            "1. ### 📌 Definition & Overview (2-3 sentences)\n"
            "2. ### 🔑 Core Key Points (Numbered list with bold technical terms)\n"
            "3. ### 💡 Exam Tip / Key Takeaway (High-yield summary for quick revision)"
        )
    }

    def generate_answer(
        self,
        question: str,
        subject_id: Optional[int] = None,
        mode: str = "detailed"
    ) -> Dict[str, Any]:
        # 1. Retrieve candidates via Hybrid Search (BM25 + Qdrant)
        candidates = hybrid_retriever.retrieve(query=question, subject_id=subject_id, top_k=20)

        if not candidates:
            return {
                "answer": self.REFUSAL_MESSAGE,
                "citations": [],
                "confidence": 0.0,
                "refused": True
            }

        # 2. Rerank using Cross-Encoder
        ranked_chunks = reranker.rerank(query=question, candidates=candidates, top_k=settings.RERANK_TOP_K)

        top_score = ranked_chunks[0].get("confidence_score", 0.0) if ranked_chunks else 0.0

        # 3. Confidence Gate Check
        if top_score < settings.CONFIDENCE_THRESHOLD:
            return {
                "answer": self.REFUSAL_MESSAGE,
                "citations": [],
                "confidence": top_score,
                "refused": True
            }

        # 4. Format Context from Top Chunks
        context_blocks = []
        for idx, chunk in enumerate(ranked_chunks, start=1):
            block = (
                f"[Chunk {idx}] Document: {chunk['filename']} | Page: {chunk['page']}\n"
                f"Content: {chunk['text']}"
            )
            context_blocks.append(block)

        context_str = "\n\n".join(context_blocks)

        # 5. Load Versioned Prompt Template
        prompt_file = "backend/app/ai/prompts/answer_prompt.txt"
        try:
            with open(prompt_file, "r", encoding="utf-8") as f:
                template = f.read()
        except Exception:
            template = "Context:\n{context}\n\nQuestion:\n{question}"

        # Inject Mode-Specific Instruction
        mode_instruction = self.MODE_INSTRUCTIONS.get(mode.lower(), self.MODE_INSTRUCTIONS["detailed"])
        full_prompt = f"{template}\n\n==================================================\n{mode_instruction}\n=================================================="

        formatted_prompt = full_prompt.format(context=context_str, question=question)

        # 6. LLM Call
        raw_answer = llm_client.generate(formatted_prompt)

        # 7. Verify Citations
        verified = citation_verifier.verify_citations(raw_answer, ranked_chunks)

        return {
            "answer": verified["verified_answer"],
            "citations": verified["citations"],
            "confidence": round(top_score, 4),
            "refused": False
        }

answer_generator = AnswerGenerator()
