import pytest
from scraper.client import ChessClient


def test_client_passes_username(real_username: str):
    client = ChessClient(real_username)

    assert client.username == real_username


def test_client_fails_on_bad_username(fake_username: str):
    with pytest.raises(ValueError):
        client = ChessClient(fake_username)


def test_client_finds_archives(client: ChessClient):
    archives = client.list_archives()

    assert isinstance(archives, list)
    assert len(archives) > 0


# def test_client_pulls_archive(client, ChessClient):
#     archives = client.list_archives()
