import os
import shutil

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.agents.batch_orchestrator_agent import BatchOrchestratorAgent
from app.agents.orchestrator_agent import OrchestratorAgent
from app.exports.candidate_ranking_exporter import export_candidates_to_csv

router = APIRouter()

orchestrator = OrchestratorAgent()
batch_orchestrator = BatchOrchestratorAgent()


@router.post("/analyze")
async def analyze(
    cv_file: UploadFile = File(...),
    ao_file: UploadFile = File(...),
    question: str = Form(""),
):
    try:
        os.makedirs("app/storage/cvs", exist_ok=True)
        os.makedirs("app/storage/aos", exist_ok=True)

        cv_path = f"app/storage/cvs/{cv_file.filename}"
        ao_path = f"app/storage/aos/{ao_file.filename}"

        with open(cv_path, "wb") as buffer:
            shutil.copyfileobj(cv_file.file, buffer)

        with open(ao_path, "wb") as buffer:
            shutil.copyfileobj(ao_file.file, buffer)

        result = await orchestrator.run(cv_path, ao_path, question)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rank_candidates")
async def rank_candidates(
    ao_file: UploadFile = File(...), cv_files: list[UploadFile] = File(...)
):
    try:
        os.makedirs("app/storage/cvs", exist_ok=True)
        os.makedirs("app/storage/aos", exist_ok=True)

        ao_path = f"app/storage/aos/{ao_file.filename}"
        with open(ao_path, "wb") as buffer:
            shutil.copyfileobj(ao_file.file, buffer)

        cv_paths = []
        for cv_file in cv_files:
            cv_path = f"app/storage/cvs/{cv_file.filename}"
            with open(cv_path, "wb") as buffer:
                shutil.copyfileobj(cv_file.file, buffer)
            cv_paths.append(cv_path)

        result = await batch_orchestrator.run(ao_path, cv_paths)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rank_candidates_csv")
async def rank_candidates_csv(
    ao_file: UploadFile = File(...), cv_files: list[UploadFile] = File(...)
):
    try:
        os.makedirs("app/storage/cvs", exist_ok=True)
        os.makedirs("app/storage/aos", exist_ok=True)

        ao_path = f"app/storage/aos/{ao_file.filename}"
        with open(ao_path, "wb") as buffer:
            shutil.copyfileobj(ao_file.file, buffer)

        cv_paths = []
        for cv_file in cv_files:
            cv_path = f"app/storage/cvs/{cv_file.filename}"
            with open(cv_path, "wb") as buffer:
                shutil.copyfileobj(cv_file.file, buffer)
            cv_paths.append(cv_path)

        result = await batch_orchestrator.run(ao_path, cv_paths)
        csv_content = export_candidates_to_csv(result["tableau"]["rows"])

        return StreamingResponse(
            iter([csv_content]),
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=ranking_candidats.csv"
            },
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
