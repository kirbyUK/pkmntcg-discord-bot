#!/usr/bin/env python3
import discord
import asyncio
import logging

client = discord.Client()

@client.event
@asyncio.coroutine
def on_ready():
	print("Logged in as '%s' (%s)" % (client.user.name, client.user.id))

@client.event
@asyncio.coroutine
def on_message(message):
	if message.content.startswith("hello") and message.author != client.user:
		yield from client.send_message(message.channel, "hello!")

def main():
	logging.basicConfig(level=logging.INFO)
	client.run("token")

if __name__ == '__main__':
	main()
