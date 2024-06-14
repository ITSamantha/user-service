import pytest
from httpx import AsyncClient

from tests.conftest import app, async_client, event_loop, setup_db, setup_and_teardown_db
