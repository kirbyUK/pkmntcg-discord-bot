#!/usr/bin/env python3
import argparse
import logging
import re
import sys
import typing

import discord

import cardbot.pokemontcg

# The maximum number of lines the bot will post to a public server in one
# message. Anything larger will be private messaged to avoid clutter
MAX_LINES = 15

# A help message listing the available commands and syntax
def cardbot_help() -> str:
	return """
```
!search [card-name]
    Gives a list of all cards matching the search
    [card-name], as well as the set code and name.

    e.g.
        !search ambipom
        !search ninja boy
        !search splash energy

!show [set-code]
    Displays the text and image of the given card
    from the given set. If you are unsure of the
    set code, find it using !search first.

    e.g.
        !show xy11-91
        !show xy11-103
        !show xy9-113

!text [set-code]
    Similar to !show, however gives just the card text
    in a copy-and-pastable format.

    e.g.
        !text xy11-91
        !text xy11-103
        !text xy9-113
```
"""

client = discord.Client()

@client.event
async def on_ready() -> None:
	print('Logged in as "{}" ({})'.format(client.user.name, client.user.id))

@client.event
async def on_message(received: discord.Message) -> typing.Union[discord.Embed, str]:
	message = ''
	recipient = received.channel

	if received.content.startswith('!help'):
		await recipient.send(cardbot_help())

	match = re.match('!search\s+(.*)$', received.content)
	if match:
		(message, results) = cardbot.pokemontcg.search(match.group(1))
		if results > MAX_LINES:
			await recipient.send(
				'Results list is too long, messaging instead'
			)
			recipient = received.author

	match = re.match('!show\s+(?:(.*)\s+)?(.*)$', received.content)
	if match:
		message = cardbot.pokemontcg.show(match.group(1), match.group(2))

	match = re.match('!text\s+(?:(.*)\s+)?(.*)$', received.content)
	if match:
		message = cardbot.pokemontcg.text(match.group(1), match.group(2))

	if type(message) == discord.embeds.Embed:
		await recipient.send(embed=message)
	elif type(message) == str and len(message) > 0:
		await recipient.send(message)

# Process commandline arguments to get the Discord API token
def args() -> str:
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	group.add_argument(
		'-t', '--token',
		help='The Discord API token'
	)
	group.add_argument(
		'-f', '--token-file',
		type=argparse.FileType('r'),
		help='A file containing the Discord API token'
	)
	args = parser.parse_args()

	if args.token:
		return args.token
	elif args.token_file:
		return args.token_file.readline().rstrip()
	else:
		print('Please specify a valid API token with -t or -f', file=sys.stderr)
		return

def main():
	token = args()
	client.run(token)

if __name__ == '__main__':
	main()
