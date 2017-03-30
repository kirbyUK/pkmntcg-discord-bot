#!/usr/bin/env python3

from setuptools import setup, find_packages

with open('LICENSE') as f:
	license = f.read()

setup(
	name='pkmntcg-discord-bot',
	version='0.1',
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
	}
)
