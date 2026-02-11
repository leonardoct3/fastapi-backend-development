from contextlib import asynccontextmanager
from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference
from app.database.session import create_database_tables
from app.api.router import router

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_database_tables()
    yield

app = FastAPI(lifespan=lifespan_handler)

app.include_router(router)

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
