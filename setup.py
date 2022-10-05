"""
setup.py pour LeJeu.
    python3 setup.py install --user
"""


from setuptools import setup, find_packages

setup(
    name = "LeJeu",
    version = "0.1.0",
    packages = find_packages("."),
    scripts=['hanabi/hanabi'],
    author = "JD. Garaud",
    author_email = "jdgaraud@onera.fr",
    description = "Hanabi game: CLI, GUI and AI",
    license="LGPL",
    keywords = "Hanabi, game, GUI, AI",
    url = "https://gitlab.ensta.fr/garaud/Hanabi",
    # could also include long_description, download_url, classifiers, etc.
)

