#!/usr/bin/env python3
import discord
import asyncio
import logging
import pokemontcg
import re

client = discord.Client()

# Gets the token from a file
def read_token(filename):
	f = open(filename, 'r')
	token = f.read()
	return token

@client.event
@asyncio.coroutine
def on_ready():
	print("Logged in as '%s' (%s)" % (client.user.name, client.user.id))

@client.event
@asyncio.coroutine
def on_message(received):
	message = ""
	recipient = received.channel

	match = re.match("!search\s+(.*)$", received.content)
	if match:
		message = pokemontcg.search(match.group(1))
		if len(message.split('\n')) > 15:
			yield from client.send_message(
				recipient,
				"Results list is too long, messaging instead"
			)
			recipient = received.author

	match = re.match("!show\s+(.*)\s+(.*)$", received.content)
	if match:
		message = pokemontcg.show(match.group(1), match.group(2))

	if len(message) > 0:
		yield from client.send_message(recipient, message)


def main():
	logging.basicConfig(level=logging.INFO)
	token = read_token("../token")
	client.run(token)

if __name__ == '__main__':
	main()
