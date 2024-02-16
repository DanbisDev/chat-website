from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from backend.routers.users import users_router
from backend.routers.chats import chats_router
from backend.database import EntityNotFoundException
from backend.database import EntityAlreadyExistsException



app = FastAPI(
    title="Pony Express",
    description="Create an API for a chat application with title \"Pony Express\" with a subset of the eventual functionality.",
    version="0.1.0",
)


app.include_router(users_router)
app.include_router(chats_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # change this as appropriate for your setup
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", include_in_schema=False)
def default() -> str:
    return HTMLResponse(
        content=f"""
        <html>
            <body>
                <h1>{app.title}</h1>
                <p>{app.description}</p>
            </body>
        </html>
        """,
    )


@app.exception_handler(EntityNotFoundException)
def handle_entity_not_found(
    _request: Request,
    exception: EntityNotFoundException,
) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={
            "detail": {
                "type": "entity_not_found",
                "entity_name": exception.entity_name,
                "entity_id": exception.entity_id,
            },
        },
    )

@app.exception_handler(EntityAlreadyExistsException)
def handle_entity_already_exists(
    _request: Request,
    exception: EntityAlreadyExistsException,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "detail": {
                "type": "duplicate_entity",
                "entity_name": exception.entity_name,
                "entity_id": exception.entity_id,
            },
        },
    )