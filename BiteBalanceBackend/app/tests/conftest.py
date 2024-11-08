
import os
import asyncio
import warnings
from loguru import logger

import alembic
import pytest
import pytest_asyncio
from alembic.config import Config
from alembic import command
from asgi_lifespan import LifespanManager
from databases import Database
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.core.global_config import app_config


from app.db.repositories import (
    MealRepository,
)



@pytest_asyncio.fixture
def platform_headers():
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


@pytest_asyncio.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="function")
def event_loop(request):
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TEST"] = "1"
    config = Config("/app/alembic.ini")
    command.upgrade(config, "head")
    yield
    # alembic.command.downgrade(config, "base")


# Create a new application for testing
@pytest_asyncio.fixture(scope="function")
async def app(apply_migrations: None) -> FastAPI:
    from app.main import app
    return app



@pytest_asyncio.fixture(scope="function")
def db(app: FastAPI) -> Database:
    return app.state.db


# HTTP Test Client
@pytest_asyncio.fixture(scope="function")
async def platform_client(app: FastAPI):
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url="http://localhost:5000",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        ) as client:
            yield client


@pytest_asyncio.fixture(scope="session")
async def client(app: FastAPI):
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture(scope="function")
async def meals_repo(db: Database) -> MealRepository:
    return MealRepository(db)