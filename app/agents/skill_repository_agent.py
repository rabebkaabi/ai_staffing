from google.adk import Agent
from pydantic import PrivateAttr

from app.mcp.oracle_mcp_server import OracleMCPServer
from app.rag.rag_pipeline import rag_store


class SkillRepositoryAgent(Agent):
    name: str = "skill_repository_agent"

    _oracle: OracleMCPServer = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._oracle = OracleMCPServer()

    async def run(self, payload: dict):
        skills = payload.get("skills", [])
        tasks = payload.get("tasks", [])

        results = {"skills": [], "tasks": []}

        for skill in skills:
            skill_name = skill.get("name", "").strip()
            skill_type = skill.get("type", "").strip().lower()

            if not skill_name or not skill_type:
                results["skills"].append(
                    {"name": skill_name, "status": "skipped_invalid_payload"}
                )
                continue

            try:
                exists = self._oracle.skill_exists(skill_name, skill_type)

                if exists:
                    results["skills"].append(
                        {
                            "name": skill_name,
                            "type": skill_type,
                            "family": skill.get("family"),
                            "status": "exists",
                        }
                    )
                else:
                    oracle_result = self._oracle.add_skill(skill)
                    results["skills"].append(
                        {
                            "name": skill_name,
                            "type": skill_type,
                            "family": skill.get("family"),
                            "status": "detected_not_inserted",
                            "oracle_result": oracle_result,
                        }
                    )

            except Exception as e:
                results["skills"].append(
                    {
                        "name": skill_name,
                        "type": skill_type,
                        "family": skill.get("family"),
                        "status": "oracle_error",
                        "error": str(e),
                    }
                )

            await rag_store(
                text=skill_name,
                metadata={
                    "entity_type": "skill",
                    "name": skill_name,
                    "type": skill_type,
                    "family": skill.get("family"),
                },
            )

        for task in tasks:
            if isinstance(task, str):
                task_name = task.strip()
            elif isinstance(task, dict):
                task_name = task.get("name", "").strip()
            else:
                task_name = ""

            if not task_name:
                results["tasks"].append(
                    {"name": task_name, "status": "skipped_invalid_payload"}
                )
                continue

            try:
                exists = self._oracle.task_exists(task_name)

                if exists:
                    results["tasks"].append({"name": task_name, "status": "exists"})
                else:
                    oracle_result = self._oracle.add_task(task_name)
                    results["tasks"].append(
                        {
                            "name": task_name,
                            "status": "added",
                            "oracle_result": oracle_result,
                        }
                    )

            except Exception as e:
                results["tasks"].append(
                    {"name": task_name, "status": "oracle_error", "error": str(e)}
                )

            await rag_store(
                text=task_name, metadata={"entity_type": "task", "name": task_name}
            )

        return results
