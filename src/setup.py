from setuptools import find_packages, setup

with open("requirements.txt", "r") as f:
    requires = f.read().split("\n")

VERSION = '0.0.0' 
DESCRIPTION = 'Chess.com scraper'

# Setting up
setup(
    name="chess", 
    version=VERSION,
    author="Stuart Watt",
    description=DESCRIPTION,
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=requires,
    include_package_data=True,
    entry_points={"console_scripts": ["chess=scraper.cli:cli"]},
)