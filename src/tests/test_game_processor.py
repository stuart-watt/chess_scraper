import pathlib
import json

import pandas as pd

from pytest_regressions.data_regression import DataRegressionFixture

from scraper.game_processing import GameProcessor


def test_game_processor_by_regression(
    real_username: str,
    testdata: pathlib.Path,
    data_regression: DataRegressionFixture,
):
    data = pd.read_json(str(testdata))

    processor = GameProcessor(real_username)
    games = processor.clean_archive(data)

    outputs = json.loads(games.to_json(orient="records"))

    data_regression.check(outputs)

def test_ratings_by_regression(
    real_username: str,
    testdata: pathlib.Path,
    data_regression: DataRegressionFixture,
):
    data = pd.read_json(str(testdata))

    processor = GameProcessor(real_username)
    games = processor.clean_archive(data)

    ratings = processor.calculate_ratings(games)

    outputs = json.loads(ratings.to_json(orient="records"))

    data_regression.check(outputs)
