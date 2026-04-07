import asyncio

from google.adk import Agent
from pydantic import PrivateAttr

from app.agents.candidate_ranking_agent import CandidateRankingAgent
from app.agents.candidate_scoring_agent import CandidateScoringAgent
from app.agents.document_processing_agent import DocumentProcessingAgent
from app.agents.matching_agent import MatchingAgent
from app.agents.reporting_agent import ReportingAgent
from app.agents.unified_extraction_agent import UnifiedExtractionAgent
from app.utils.cache_manager import CacheManager
from app.utils.file_hash import compute_file_hash


class BatchOrchestratorAgent(Agent):
    name: str = "batch_orchestrator_agent"

    _document_processing_agent: DocumentProcessingAgent = PrivateAttr()
    _unified_extraction_agent: UnifiedExtractionAgent = PrivateAttr()
    _matching_agent: MatchingAgent = PrivateAttr()
    _candidate_scoring_agent: CandidateScoringAgent = PrivateAttr()
    _candidate_ranking_agent: CandidateRankingAgent = PrivateAttr()
    _reporting_agent: ReportingAgent = PrivateAttr()
    _cache_manager: CacheManager = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._document_processing_agent = DocumentProcessingAgent()
        self._unified_extraction_agent = UnifiedExtractionAgent()
        self._matching_agent = MatchingAgent()
        self._candidate_scoring_agent = CandidateScoringAgent()
        self._candidate_ranking_agent = CandidateRankingAgent()
        self._reporting_agent = ReportingAgent()
        self._cache_manager = CacheManager()

    async def _analyze_document(self, file_path: str, document_type: str):
        file_hash = compute_file_hash(file_path)
        cached = self._cache_manager.get_extracted(file_hash)

        if cached:
            return {
                "text": cached["text"],
                "skills": cached["skills"],
                "tasks": cached["tasks"],
            }
        processed = await self._document_processing_agent.run(file_path, document_type)
        analysis = await self._unified_extraction_agent.run(processed["text"])

        skills = analysis.get("skills", [])
        tasks = {"tasks": analysis.get("tasks", [])}

        self._cache_manager.set_extracted(
            file_hash, {"text": processed["text"], "skills": skills, "tasks": tasks}
        )

        return {"text": processed["text"], "skills": skills, "tasks": tasks}

    async def run(self, ao_path: str, cv_paths: list[str]):
        ao_result = await self._analyze_document(ao_path, "ao")

        async def score_one_candidate(cv_path: str):
            cv_result = await self._analyze_document(cv_path, "cv")

            matching_result = await self._matching_agent.run(
                {
                    "cv_text": cv_result["text"],
                    "ao_text": ao_result["text"],
                    "cv_skills": cv_result["skills"],
                    "ao_skills": ao_result["skills"],
                    "cv_tasks": cv_result["tasks"],
                    "ao_tasks": ao_result["tasks"],
                }
            )

            scoring_result = await self._candidate_scoring_agent.run(
                {
                    "cv_text": cv_result["text"],
                    "ao_text": ao_result["text"],
                    "cv_skills": cv_result["skills"],
                    "ao_skills": ao_result["skills"],
                    "cv_tasks": cv_result["tasks"],
                    "ao_tasks": ao_result["tasks"],
                    "matching_result": matching_result,
                }
            )

            return scoring_result

        candidates = await asyncio.gather(
            *[score_one_candidate(cv_path) for cv_path in cv_paths]
        )

        ranked_candidates = await self._candidate_ranking_agent.run(candidates)
        report = await self._reporting_agent.run(ranked_candidates)

        return {
            "ao_file": ao_path,
            "nombre_candidats": len(cv_paths),
            "ranking": ranked_candidates,
            "tableau": report,
        }
