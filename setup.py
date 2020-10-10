"""Package setup file."""
from setuptools import setup, find_packages

with open("LICENSE") as f:
    license = f.read()

setup(
    name="pkmntcg-discord-bot",
    version="0.6",
    description="A Discord bot for searching and displaying Pokemon TCG cards",
    author="Alex Kerr",
    author_email="kirby@cpan.org",
    url="https://github.com/kirbyUK/pkmntcg-discord-bot",
    license=license,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "cardbot=cardbot.main:main"
        ]
    },
    install_requires=[
        "discord.py>=1.3.1",
        "pokemontcgsdk>=2.0.0",
    ]
)
