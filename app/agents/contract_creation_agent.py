from google.adk import Agent

from app.llm.gemini_client import ask_gemini


class ContractCreationAgent(Agent):

    name: str = "contract_creation_agent"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def run(self, decision):

        with open("app/prompts/contract_generation.txt", "r", encoding="utf-8") as f:
            template = f.read()

        prompt = template.replace("{decision}", str(decision))

        return await ask_gemini(prompt)
