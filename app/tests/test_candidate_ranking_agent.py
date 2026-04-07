import pytest

from app.agents.candidate_ranking_agent import CandidateRankingAgent


@pytest.mark.asyncio
async def test_candidate_ranking_agent_sorts_candidates_by_score():
    agent = CandidateRankingAgent()

    candidates = [
        {"nom": "A", "score_similarite": 70},
        {"nom": "B", "score_similarite": 92},
        {"nom": "C", "score_similarite": 81},
    ]

    result = await agent.run(candidates)

    assert result[0]["nom"] == "B"
    assert result[1]["nom"] == "C"
    assert result[2]["nom"] == "A"
    assert result[0]["rang"] == 1
    assert result[1]["rang"] == 2
    assert result[2]["rang"] == 3
