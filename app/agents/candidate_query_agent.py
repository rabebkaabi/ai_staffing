from google.adk import Agent

from app.llm.gemini_client import ask_gemini
from app.rag.rag_pipeline import rag_search


class CandidateQueryAgent(Agent):
    name: str = "candidate_query_agent"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def run(self, payload: dict):
        question = payload.get("question", "")
        cv_path = payload.get("cv_path")
        ao_path = payload.get("ao_path")

        cv_results = await rag_search(
            query=question,
            top_k=5,
            filters={"document_type": "cv", "source_path": cv_path},
        )

        ao_results = await rag_search(
            query=question,
            top_k=5,
            filters={"document_type": "ao", "source_path": ao_path},
        )

        cv_context = "\n\n".join(
            item["metadata"].get("chunk_text", "") for item in cv_results
        )

        ao_context = "\n\n".join(
            item["metadata"].get("chunk_text", "") for item in ao_results
        )

        with open("app/prompts/candidate_query_prompt.txt", "r", encoding="utf-8") as f:
            template = f.read()

        prompt = (
            template.replace("{question}", str(question))
            .replace("{cv_skills}", str(payload.get("cv_skills", [])))
            .replace("{ao_skills}", str(payload.get("ao_skills", [])))
            .replace("{cv_tasks}", str(payload.get("cv_tasks", {})))
            .replace("{ao_tasks}", str(payload.get("ao_tasks", {})))
            .replace("{matching_result}", str(payload.get("matching_result", {})))
            .replace("{cv_context}", cv_context)
            .replace("{ao_context}", ao_context)
        )

        return await ask_gemini(prompt)
