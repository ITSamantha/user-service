import asyncio
import os
from typing import Generator, Any

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from sqlalchemy_utils import database_exists, drop_database

from src.apps.employees.models import *
from src.core.database.base import Base
from src.core.database.session_manager import db_manager

from src.main import get_application

db_manager.initialize(prod=False)


@pytest.fixture(scope='session')
def event_loop():
    policy = asyncio.WindowsSelectorEventLoopPolicy()
    asyncio.set_event_loop_policy(policy)
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    db_manager.initialize(prod=False)
    yield
    db_manager.initialize(prod=True)


@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_db():
    async def _create_tables():
        try:
            async with db_manager.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                print("Tables created successfully")
        except Exception as e:
            print(f"Error creating tables: {e}")

    async def _drop_tables():
        try:
            async with db_manager.engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                print("Tables dropped successfully")
            os.remove("test.db")  # TODO: CHANGE

            print("Database dropped successfully")
        except Exception as e:
            print(f"Error dropping tables: {e}")

    asyncio.run(_create_tables())

    yield

    asyncio.run(_drop_tables())


@pytest.fixture(scope="function")
async def app() -> Generator[FastAPI, Any, None]:
    _app = get_application()
    yield _app


@pytest.fixture(scope="function")
async def async_client(app):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def anyio_backend():
    return 'asyncio'
