from google.adk import Agent


class ReportingAgent(Agent):
    name: str = "reporting_agent"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def run(self, ranked_candidates: list[dict]):
        rows = []

        for candidate in ranked_candidates:
            rows.append(
                {
                    "nom": candidate.get("nom", ""),
                    "prenom": candidate.get("prenom", ""),
                    "profil": candidate.get("profil", ""),
                    "competences": ", ".join(candidate.get("competences", [])),
                    "taches": ", ".join(candidate.get("taches", [])),
                    "ecarts": ", ".join(candidate.get("ecarts", [])),
                    "score_similarite": candidate.get("score_similarite", 0),
                    "rang": candidate.get("rang", 0),
                    "decision_ia": candidate.get("decision_ia", ""),
                }
            )

        return {
            "columns": [
                "nom",
                "prenom",
                "profil",
                "competences",
                "taches",
                "ecarts",
                "score_similarite",
                "rang",
                "decision_ia",
            ],
            "rows": rows,
        }
