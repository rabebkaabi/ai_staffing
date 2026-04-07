from google.adk import Agent

from app.llm.gemini_client import ask_gemini_json


class CandidateScoringAgent(Agent):
    name: str = "candidate_scoring_agent"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def run(self, payload: dict):
        with open(
            "app/prompts/candidate_scoring_prompt.txt", "r", encoding="utf-8"
        ) as f:
            template = f.read()

        prompt = (
            template.replace("{cv_text}", str(payload.get("cv_text", "")))
            .replace("{ao_text}", str(payload.get("ao_text", "")))
            .replace("{cv_skills}", str(payload.get("cv_skills", [])))
            .replace("{ao_skills}", str(payload.get("ao_skills", [])))
            .replace("{cv_tasks}", str(payload.get("cv_tasks", {})))
            .replace("{ao_tasks}", str(payload.get("ao_tasks", {})))
            .replace("{matching_result}", str(payload.get("matching_result", {})))
        )

        return await ask_gemini_json(prompt)
