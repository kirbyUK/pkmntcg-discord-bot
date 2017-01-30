#!/usr/bin/env python3
import discord
import asyncio
import logging
import pokemontcg
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

!show [card-name] [set-code]
	Displays the text and image of the given card
	from the given set. If you are unsure of the
	set code, find it using !search first.

	e.g.
		!show ambipom xy11
		!show ninja boy xy11
		!show splash energy xy9
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
		recipient = received.author
		message = cardbot_help()

	match = re.match("!search\s+(.*)$", received.content)
	if match:
		message = pokemontcg.search(match.group(1))
		if len(message.split('\n')) - 1 > MAX_LINES:
			yield from client.send_message(
				recipient,
				"Results list is too long, messaging instead"
			)
			recipient = received.author

	match = re.match("!show\s+(.*)\s+(.*)$", received.content)
	if match:
		message = pokemontcg.show(match.group(1), match.group(2))

#	match = re.match("!show\s+(.*-.*)$", received.content)
#	if match:
#		message = pokemontcg.show("", match.group(1))

	if len(message) > 0:
		yield from client.send_message(recipient, message)


def main():
	logging.basicConfig(level=logging.INFO)
	token = read_token("../token")
	client.run(token)

if __name__ == '__main__':
	main()
