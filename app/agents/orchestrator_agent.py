import asyncio

from google.adk import Agent
from pydantic import PrivateAttr

from app.agents.candidate_query_agent import CandidateQueryAgent
from app.agents.contract_creation_agent import ContractCreationAgent
from app.agents.contract_decision_agent import ContractDecisionAgent
from app.agents.document_processing_agent import DocumentProcessingAgent
from app.agents.matching_agent import MatchingAgent
from app.agents.unified_extraction_agent import UnifiedExtractionAgent
from app.utils.cache_manager import CacheManager
from app.utils.file_hash import compute_file_hash


class OrchestratorAgent(Agent):
    name: str = "orchestrator_agent"

    _doc_agent: DocumentProcessingAgent = PrivateAttr()
    _extract_agent: UnifiedExtractionAgent = PrivateAttr()
    _match_agent: MatchingAgent = PrivateAttr()
    _query_agent: CandidateQueryAgent = PrivateAttr()
    _decision_agent: ContractDecisionAgent = PrivateAttr()
    _contract_agent: ContractCreationAgent = PrivateAttr()
    _cache: CacheManager = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._doc_agent = DocumentProcessingAgent()
        self._extract_agent = UnifiedExtractionAgent()
        self._match_agent = MatchingAgent()
        self._query_agent = CandidateQueryAgent()
        self._decision_agent = ContractDecisionAgent()
        self._contract_agent = ContractCreationAgent()
        self._cache = CacheManager()

    async def _analyze_document(self, file_path: str, doc_type: str):
        file_hash = compute_file_hash(file_path)
        cached = self._cache.get_extracted(file_hash)

        if cached:
            return {
                "text": cached["text"],
                "skills": cached["skills"],
                "tasks": cached["tasks"],
                "cache": "hit",
            }

        processed = await self._doc_agent.run(file_path, doc_type)
        extracted = await self._extract_agent.run(processed["text"])

        result = {
            "text": processed["text"],
            "skills": extracted.get("skills", []),
            "tasks": {"tasks": extracted.get("tasks", [])},
            "cache": "miss",
        }

        self._cache.set_extracted(file_hash, result)

        return result

    async def run(self, cv_path: str, ao_path: str, question: str | None = None):
        # PARALLÉLISATION
        cv, ao = await asyncio.gather(
            self._analyze_document(cv_path, "cv"), self._analyze_document(ao_path, "ao")
        )

        # MATCHING
        matching = await self._match_agent.run(
            {
                "cv_text": cv["text"],
                "ao_text": ao["text"],
                "cv_skills": cv["skills"],
                "ao_skills": ao["skills"],
                "cv_tasks": cv["tasks"],
                "ao_tasks": ao["tasks"],
            }
        )

        # DECISION
        decision = await self._decision_agent.run(matching)

        # CONTRAT
        contract = await self._contract_agent.run(decision)

        # QUESTION COMMERCIALE
        answer = None
        if question and question.strip():
            answer = await self._query_agent.run(
                {
                    "question": question,
                    "cv_path": cv_path,
                    "ao_path": ao_path,
                    "cv_skills": cv["skills"],
                    "ao_skills": ao["skills"],
                    "cv_tasks": cv["tasks"],
                    "ao_tasks": ao["tasks"],
                    "matching_result": matching,
                }
            )

        return {
            "metadata": {
                "cv_cache": cv["cache"],
                "ao_cache": ao["cache"],
            },
            "extraction": {
                "cv_skills": cv["skills"],
                "ao_skills": ao["skills"],
                "cv_tasks": cv["tasks"],
                "ao_tasks": ao["tasks"],
            },
            "matching": matching,
            "contract": {"decision": decision, "generated": contract},
            "reponse_commerciale": answer,
        }
