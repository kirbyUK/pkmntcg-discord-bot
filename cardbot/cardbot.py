#!/usr/bin/env python3
import discord
import asyncio
import logging
import pokemontcg
import re

client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
	print("Logged in as '%s' (%s)" % (client.user.name, client.user.id))

@client.event
@asyncio.coroutine
def on_message(message):
	match = re.match("!search\s+(.*)$", message.content)
	if match:
		yield from client.send_message(
			message.channel,
			pokemontcg.search(match.group(1))
		)

	match = re.match("!show\s+(.*)\s+(.*)$", message.content)
	if match:
		yield from client.send_message(
			message.channel,
			pokemontcg.show(match.group(1), match.group(2))
		)


def main():
	logging.basicConfig(level=logging.INFO)
	client.run("token")

if __name__ == '__main__':
	main()
