from fastapi import FastAPI

from app.routes.health import router

app = FastAPI()

app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "Enterprise Visual Intelligence API"}
