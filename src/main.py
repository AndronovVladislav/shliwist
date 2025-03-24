import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from src.config import settings
from src.models.utils import db_helper
from src.routes.auth.auth import router as auth_router
from src.routes.wishlist import router as wishlist_router


@asynccontextmanager
async def lifespan(app: FastAPI):  # pylint: disable=W0621,W0613
    yield
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(wishlist_router)

Instrumentator().instrument(app).expose(app)


@app.get('/healthcheck')
async def healthcheck():
    return {'status': 'ok'}


@app.get("/whoami")
def whoami():
    return {"pod": os.getenv("HOSTNAME")}


if __name__ == '__main__':
    uvicorn.run(app,
                host=settings.uvicorn.host,
                port=settings.uvicorn.port,
                workers=settings.uvicorn.workers,
                timeout_keep_alive=settings.uvicorn.timeout,
                )
