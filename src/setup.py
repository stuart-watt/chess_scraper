from setuptools import find_packages, setup

with open("scraper/requirements.txt", "r") as f:
    requires = f.read().split("\n")

DESCRIPTION = "Scrapes game data from chess.com"

# Setting up
setup(
    name="chess_scraper",
    description=DESCRIPTION,
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=requires,
    include_package_data=True,
    entry_points={"console_scripts": ["chess_scraper=scraper.scraper:main"]},
)
