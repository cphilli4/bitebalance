import uuid

from fastapi import FastAPI, Request

from starlette.middleware.cors import CORSMiddleware

from app.core import (
    create_start_app_handler,
    create_stop_app_handler,
)
from app.core.global_config import app_config
from app.logger import setup_logging

# Add app defined exceptions

from app.modules import application_module, users_module

global consumer

app = FastAPI(
    title="BiteBalance API",
    version=app_config.API_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Inject Request Ids
@app.middleware("http")
async def request_middleware(request: Request, call_next):
    request.state.request_id = uuid.uuid4().hex
    request.state.request_ip = request.client.host
    request.state.request_method = request.method
    # add record here.!
    response = await call_next(request)
    return response

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_event_handler("startup", setup_logging)

# Database Connection
app.add_event_handler("startup", create_start_app_handler(app))
app.add_event_handler("shutdown", create_stop_app_handler(app))

app.add_event_handler("startup", users_module.mount(app))
app.add_event_handler("startup", application_module.mount(app))
