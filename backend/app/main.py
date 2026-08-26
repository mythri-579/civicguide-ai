from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

from app.database import Base, engine, SessionLocal
from app.routes import document_routes, chat_routes, eligibility_routes, update_routes, auth_routes
from app.services.update_monitor_service import check_all_sources

Base.metadata.create_all(bind=engine)

scheduler = BackgroundScheduler()


def scheduled_source_check():
    db = SessionLocal()
    try:
        result = check_all_sources(db)
        print(f"[Scheduler] Weekly source check completed: {result}")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(scheduled_source_check, "interval", weeks=1, id="weekly_source_check")
    scheduler.start()
    print("[Scheduler] Started — weekly source check job scheduled.")
    yield
    scheduler.shutdown()
    print("[Scheduler] Stopped.")


app = FastAPI(title="CivicGuide AI", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(document_routes.router)
app.include_router(chat_routes.router)
app.include_router(eligibility_routes.router)
app.include_router(update_routes.router)
app.include_router(auth_routes.router)


@app.get("/")
def home():
    return {"message": "CivicGuide AI backend is running"}