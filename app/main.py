from fastapi import FastAPI

from app.routes.analyze import router as analyze_router
from app.routes.health import router as health_router
from app.routes.reports import router as reports_router

app = FastAPI()

app.include_router(health_router)
app.include_router(analyze_router)
app.include_router(reports_router)


@app.get("/")
def read_root():
    return {"message": "Enterprise Visual Intelligence API"}
