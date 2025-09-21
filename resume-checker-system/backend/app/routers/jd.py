from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.jd_schema import JD
from app.models.models import Job
from app.db.database import get_db

router = APIRouter()

@router.post("/upload")
def upload_jd(jd: JD, db: Session = Depends(get_db)):
    db_job = Job(
        title=jd.title, 
        description=jd.description,
        location=jd.location,
        must_have=",".join(jd.must_have) if jd.must_have else None,
        good_to_have=",".join(jd.good_to_have) if jd.good_to_have else None
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/list")
def list_jds(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return [
        {
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "location": job.location,
            "must_have": job.must_have.split(",") if job.must_have else [],
            "good_to_have": job.good_to_have.split(",") if job.good_to_have else []
        }
        for job in jobs
    ]