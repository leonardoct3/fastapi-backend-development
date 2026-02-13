from contextlib import asynccontextmanager
from fastapi import BackgroundTasks, FastAPI
from scalar_fastapi import get_scalar_api_reference
from app.database.session import create_database_tables
from app.api.router import master_router
from app.services.notification import NotificationService

@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    await create_database_tables()
    yield

app = FastAPI(lifespan=lifespan_handler)

app.include_router(master_router)

@app.get("/mail")
async def send_test_mail(tasks: BackgroundTasks):
    
    tasks.add_task(
        NotificationService().send_message,
        recipients=["carvalho.leonardo@bcg.com"],
        subject="Test Mail",
        body="Anything"
    )

    return {"detail": "Sending email... 👊"}

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
