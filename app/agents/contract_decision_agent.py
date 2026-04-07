from google.adk import Agent

from app.llm.gemini_client import ask_gemini_json


class ContractDecisionAgent(Agent):

    name: str = "contract_decision_agent"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def run(self, matching_result):

        with open("app/prompts/contract_decision.txt", "r", encoding="utf-8") as f:
            template = f.read()

        prompt = template.replace("{result}", str(matching_result))

        return await ask_gemini_json(prompt)
