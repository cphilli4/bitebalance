
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


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
def apply_migrations():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    # os.environ["TEST"] = "1"
    config = Config("/app/alembic.ini")
    script_location = "/app/db/migrations"
    config.set_main_option("script_location", script_location)
    command.upgrade(config, "head")
    yield
    # alembic.command.downgrade(config, "base")


# Create a new application for testing
@pytest_asyncio.fixture(scope="session")
async def app(apply_migrations: None) -> FastAPI:
    from app.main import app
    db_username, db_password = (app_config.POSTGRES_USER, app_config.POSTGRES_PASSWORD)
    database_url = (
        f"postgresql+asyncpg://{db_username}:{db_password}@{app_config.POSTGRES_SERVER}"
        f":{app_config.POSTGRES_PORT}/{app_config.POSTGRES_DB}"
    )
    logger.info(
            "  ---------- STARTING APP IN TEST MODE -----------------{}".format(str(app.state))
        )
    logger.info(
            "--- DB CONNECTION database_url TO {}---".format(database_url)
        )
    database = Database(
        database_url, min_size=2, max_size=10
    )  # these can be app_configured in app_config as well
    try:
        await database.connect()
        app.state.db = database
        logger.info(
            "--- DB CONNECTION ESTABLISHED TO {}---".format(app_config.POSTGRES_SERVER)
        )
    except Exception as e:
        logger.warning("--- DB CONNECTION ERROR ---")
        logger.warning(e)
        logger.warning("--- DB CONNECTION ERROR ---")
    return app



@pytest_asyncio.fixture(scope="session")
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


@pytest_asyncio.fixture(scope="session")
async def meals_repo(db: Database) -> MealRepository:
    return MealRepository(db)