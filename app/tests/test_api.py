from fastapi.testclient import TestClient

from app.main import app


def test_home_page_loads():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200


def test_docs_load():
    client = TestClient(app)
    response = client.get("/docs")

    assert response.status_code == 200


def test_analyze_endpoint(monkeypatch):
    client = TestClient(app)

    async def fake_run(cv_path: str, ao_path: str, question: str = ""):
        return {
            "metadata": {"cv_cache": "miss", "ao_cache": "miss"},
            "extraction": {
                "cv_skills": [{"name": "Python", "type": "technical", "family": "MOE"}],
                "ao_skills": [{"name": "Python", "type": "technical", "family": "MOE"}],
                "cv_tasks": {"tasks": ["Développement API"]},
                "ao_tasks": {"tasks": ["Développement API"]},
            },
            "matching": {
                "score": 90,
                "resume": "Très bon matching",
                "competences_manquantes": [],
                "positionnement_candidat": "Profil MOE backend",
                "reponse_commerciale": "Profil très adapté.",
            },
            "contract": {
                "decision": {"recommandation": "Oui", "justification": "Bon fit"},
                "generated": "Synthèse contractuelle",
            },
            "reponse_commerciale": None,
        }

    monkeypatch.setattr("app.api.matching_api.orchestrator.run", fake_run)

    files = {
        "cv_file": (
            "cv.txt",
            b"Developpeur Python backend",
            "text/plain",
        ),
        "ao_file": (
            "ao.txt",
            b"Recherche developpeur Python",
            "text/plain",
        ),
    }

    response = client.post("/analyze", files=files, data={"question": ""})

    assert response.status_code == 200
    payload = response.json()
    assert payload["matching"]["score"] == 90


def test_rank_candidates_endpoint(monkeypatch):
    client = TestClient(app)

    async def fake_batch_run(ao_path: str, cv_paths: list[str]):
        return {
            "ao_file": ao_path,
            "nombre_candidats": 2,
            "ranking": [
                {"nom": "A", "score_similarite": 91, "rang": 1},
                {"nom": "B", "score_similarite": 76, "rang": 2},
            ],
            "tableau": {
                "columns": ["nom", "score_similarite", "rang"],
                "rows": [
                    {"nom": "A", "score_similarite": 91, "rang": 1},
                    {"nom": "B", "score_similarite": 76, "rang": 2},
                ],
            },
        }

    monkeypatch.setattr("app.api.matching_api.batch_orchestrator.run", fake_batch_run)

    files = [
        ("ao_file", ("ao.txt", b"Recherche dev Python", "text/plain")),
        ("cv_files", ("cv1.txt", b"CV 1 Python", "text/plain")),
        ("cv_files", ("cv2.txt", b"CV 2 Java", "text/plain")),
    ]

    response = client.post("/rank_candidates", files=files)

    assert response.status_code == 200
    payload = response.json()
    assert payload["nombre_candidats"] == 2
    assert payload["ranking"][0]["rang"] == 1