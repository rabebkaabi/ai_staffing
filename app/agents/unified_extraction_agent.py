from google.adk import Agent

from app.llm.gemini_client import ask_gemini_json


class UnifiedExtractionAgent(Agent):
    name: str = "unified_extraction_agent"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def run(self, text: str):
        # Sécurité input
        if not text or not text.strip():
            return {"skills": [], "tasks": []}

        try:
            # Chargement du prompt
            with open(
                "app/prompts/unified_extraction_prompt.txt", "r", encoding="utf-8"
            ) as f:
                template = f.read()

            prompt = template.replace("{document}", text)

            # Appel LLM
            result = await ask_gemini_json(prompt)

            # Sécurisation output
            skills = result.get("skills", [])
            tasks = result.get("tasks", [])

            # Nettoyage minimal
            if not isinstance(skills, list):
                skills = []
            if not isinstance(tasks, list):
                tasks = []

            return {"skills": skills, "tasks": tasks}

        except Exception as e:
            # Fallback robuste (important en prod)
            return {"skills": [], "tasks": [], "error": str(e)}
