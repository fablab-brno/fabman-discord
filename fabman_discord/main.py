from fastapi import FastAPI

from . import fabman

app = FastAPI()
app.include_router(
    fabman.router,
    prefix="/fabman",
)


@app.get("/status")
def read_root():
    return "ok"
