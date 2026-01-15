from fastapi import APIRouter
from app.scripts.fine_tuning_pipeline import FineTuningPipeline

router = APIRouter()

@router.post("/trigger")
async def trigger_training():
    pipeline = FineTuningPipeline(bucket_name="llmops-long-term-memory")
    # In a real scenario, this would be an async background task
    # job = pipeline.start_fine_tuning_job(...)
    return {"status": "Training job triggered", "job_id": "dummy-job-123"}
