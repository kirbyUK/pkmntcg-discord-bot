#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('LICENSE') as f:
	license = f.read()

setup(
	name='pkmntcg-discord-bot',
	version='0.3',
	description='A Discord bot for searching and displaying Pokemon TCG cards',
	author='Alex Kerr',
	author_email='kirby@cpan.org',
	url='https://github.com/kirbyUK/pkmntcg-discord-bot',
	license=license,
	packages=[ 'cardbot' ],
	entry_points={
		'console_scripts' : [
			'cardbot = cardbot.cardbot:main'
		]
	},
	install_requires=[
		'aiohttp<1.1.0,>=1.0.5',
		'async-timeout>=1.1.0',
		'chardet>=2.3.0',
		'discord.py>=0.16.12',
		'multidict>=2.1.4',
		'pokemontcgsdk>=2.0.0',
		'websockets<4.0,>=3.2'
	]
)
