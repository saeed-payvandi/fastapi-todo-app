from fastapi import FastAPI
from contextlib import asynccontextmanager
from tasks.routes import router as tasks_routes
from users.routes import router as users_routes

tags_metadata = [
    {
        "name": "tasks",
        "description": "Operation related to tasks managment",
        "externalDocs": {
            "description": "More about tasks",
            "url": "https:/example.com/docs/tasks",
        }
    }
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application startup")
    yield
    print("Application shutdown")

app = FastAPI(
    lifespan=lifespan,
    openapi_tags=tags_metadata,
    title="Todo Application",
    description="A task management application for creating, updating, and tracking tasks",
    summary="Manage your tasks efficiently",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Example Name",
        "url": "https://example.com/contact/",
        "email": "contact@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://license.org/mit/",
    },
)

# app.include_router(tasks_routes, prefix="/api/v1")
app.include_router(tasks_routes)
app.include_router(users_routes)
