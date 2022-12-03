from uuid import uuid4

import pytest

from scraper.client import ChessClient
from scraper.utils import GameProcessor


@pytest.fixture
def real_username() -> str:
    return "samwise_gambit"


@pytest.fixture
def fake_username() -> str:
    # It is highly unlikely that a user has this username
    return uuid4().hex


@pytest.fixture
def client(real_username: str) -> ChessClient:
    return ChessClient(real_username)


@pytest.fixture
def proccesor(real_username: str) -> GameProcessor:
    return GameProcessor(real_username)
