import pandas as pd

import pytest
from pytest_regressions.data_regression import DataRegressionFixture

from scraper.chess_client import ChessClient


def test_client_passes_username(real_username: str):
    client = ChessClient(real_username)

    assert client.username == real_username


def test_client_fails_on_bad_username(fake_username: str):
    with pytest.raises(ValueError):
        client = ChessClient(fake_username)


def test_client_finds_archives(client: ChessClient):
    archives = client.list_archives()

    assert isinstance(archives, list)
    assert isinstance(archives[0], str)
    assert len(archives) > 0


def test_client_pulls_archive(
    client: ChessClient, data_regression: DataRegressionFixture
):

    archives = client.list_archives()
    data = client.get_archive(archives[0])

    assert isinstance(data, list)
    assert len(data) > 0

    data_regression.check(data)
