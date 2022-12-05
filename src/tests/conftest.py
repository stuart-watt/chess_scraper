from uuid import uuid4
import pathlib

import pytest

from scraper.chess_client import ChessClient
from scraper.game_processing import GameProcessor


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


@pytest.fixture
def testdata() -> pathlib.Path:
    return pathlib.Path(__file__).parent / "data/test.json"
