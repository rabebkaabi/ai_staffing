import pytest

from app.agents.matching_agent import MatchingAgent


@pytest.mark.asyncio
async def test_matching_agent_returns_mocked_json(monkeypatch, tmp_path):
    prompt_dir = tmp_path / "app" / "prompts"
    prompt_dir.mkdir(parents=True, exist_ok=True)

    (prompt_dir / "matching_prompt.txt").write_text(
        """CV TEXTE: {cv_text}
AO TEXTE: {ao_text}
CV COMPETENCES: {cv_skills}
AO COMPETENCES: {ao_skills}
CV TACHES: {cv_tasks}
AO TACHES: {ao_tasks}""",
        encoding="utf-8",
    )

    monkeypatch.chdir(tmp_path)

    async def fake_ask_gemini_json(prompt: str):
        assert "python" in prompt.lower()
        return {
            "score": 85,
            "resume": "Bon matching",
            "correspondance_competences": ["Python"],
            "correspondance_taches": ["Développement API"],
            "competences_manquantes": ["Docker"],
            "points_forts": ["Expérience backend"],
            "positionnement_candidat": "Profil MOE orienté backend",
            "competences_techniques": ["Python"],
            "competences_fonctionnelles": [],
            "famille_principale": "MOE",
            "sous_famille_fonctionnelle": "",
            "decision": "adapté",
            "reponse_commerciale": "Profil pertinent pour la mission.",
        }

    monkeypatch.setattr(
        "app.agents.matching_agent.ask_gemini_json",
        fake_ask_gemini_json,
    )

    agent = MatchingAgent()
    result = await agent.run(
        {
            "cv_text": "Développeur Python backend",
            "ao_text": "Recherche développeur Python",
            "cv_skills": [{"name": "Python", "type": "technical", "family": "MOE"}],
            "ao_skills": [{"name": "Python", "type": "technical", "family": "MOE"}],
            "cv_tasks": {"tasks": ["Développement API"]},
            "ao_tasks": {"tasks": ["Développement API"]},
        }
    )

    assert result["score"] == 85
    assert result["decision"] == "adapté"
    assert "Python" in result["correspondance_competences"]
