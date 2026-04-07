from google.adk import Agent


class CandidateRankingAgent(Agent):
    name: str = "candidate_ranking_agent"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def run(self, candidates: list[dict]):
        sorted_candidates = sorted(
            candidates, key=lambda x: x.get("score_similarite", 0), reverse=True
        )

        for idx, candidate in enumerate(sorted_candidates, start=1):
            candidate["rang"] = idx

        return sorted_candidates
