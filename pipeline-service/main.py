from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db, init_db
from services.ingestion import fetch_all_customers, upsert_customers


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="FlowSync Pipeline", version="1.0.0", lifespan=lifespan)


@app.get("/api/health")
def health():
    return {"status": "healthy", "service": "pipeline-service"}


@app.post("/api/ingest")
def ingest(db: Session = Depends(get_db)):
    try:
        customers = fetch_all_customers()
        count = upsert_customers(db, customers)
        return {"status": "success", "records_processed": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
