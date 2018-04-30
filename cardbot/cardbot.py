#!/usr/bin/env python3
import argparse
import discord
import asyncio
import logging
import cardbot.pokemontcg
import re

# The maximum number of lines the bot will post to a public server in one
# message. Anything larger will be private messaged to avoid clutter
MAX_LINES = 15

client = discord.Client()

# Gets the token from a file
def read_token(filename):
	f = open(filename, 'r')
	token = f.read()
	return token

# A help message listing the available commands and syntax
def cardbot_help():
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
    Similar to !show, however gives just the text in
    a copy-and-pastable format.

    e.g.
        !show xy11-91
        !show xy11-103
        !show xy9-113
```
	"""

@client.event
@asyncio.coroutine
def on_ready():
	print("Logged in as '%s' (%s)" % (client.user.name, client.user.id))

@client.event
@asyncio.coroutine
def on_message(received):
	message = ""
	recipient = received.channel

	if received.content.startswith("!help"):
		yield from client.send_message(received.author, cardbot_help())

	match = re.match("!search\s+(.*)$", received.content)
	if match:
		(message, results) = cardbot.pokemontcg.search(match.group(1))
		if results > MAX_LINES:
			yield from client.send_message(
				recipient,
				"Results list is too long, messaging instead"
			)
			recipient = received.author
		if type(message) == discord.embeds.Embed:
			yield from client.send_message(recipient, embed=message)
		else:
			yield from client.send_message(recipient, message)

	match = re.match("!show\s+(?:(.*)\s+)?(.*)$", received.content)
	if match:
		message = cardbot.pokemontcg.show(match.group(1), match.group(2))
		if type(message) == str and len(message) > 0:
			yield from client.send_message(recipient, message)
		elif type(message) != str:
			yield from client.send_message(recipient, embed=message)

	match = re.match("!text\s+(?:(.*)\s+)?(.*)$", received.content)
	if match:
		message = cardbot.pokemontcg.text(match.group(1), match.group(2))
		if type(message) == str and len(message) > 0:
			yield from client.send_message(recipient, message)


def main():
	# Process command-line arguments to get the token
	parser = argparse.ArgumentParser()
	group = parser.add_mutually_exclusive_group()
	group.add_argument('-t', '--token', help='The Discord API token')
	group.add_argument('-f', '--token-file',
		help='A file containing the Discord API token')
	args = parser.parse_args()
	if args.token:
		token = args.token
	elif args.token_file:
		token = read_token(args.token_file)
	else:
		print("Please specify a valid API token with -t or -f")
		return

	logging.basicConfig(level=logging.INFO)
	client.run(token)

if __name__ == '__main__':
	main()
