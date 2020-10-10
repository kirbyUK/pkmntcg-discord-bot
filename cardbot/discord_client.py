"""Module defining the Discord client and its event handlers."""
import re
from typing import Callable, Dict

import discord

from cardbot.commands import cardbot_help, cardbot_search, cardbot_show


"""The Discord client object."""
client = discord.Client()


@client.event
async def on_ready() -> None:
    """Discord ready event handler, prints a logged in message."""
    print(f"Logged in as '{client.user.name}' ({client.user.id})")


@client.event
async def on_message(received: discord.Message) -> None:
    """
    Discord message handler.

    :param received: The received Discord message.
    """
    recipient = received.channel

    # Mapping of the command regex to the implementing function of the command
    commands: Dict[str, Callable[..., discord.Embed]] = {
        r"!help": cardbot_help,
        r"!search\s+(.*)$": cardbot_search,
        r"!show\s+(.*)$": cardbot_show,
    }

    # Find the matching command
    for regex in commands:
        m = re.match(regex, received.content)
        if m:
            # Unpack the arguments to the implementing function, get a response,
            # and send it back with the Discord client
            message = commands[regex](*m.groups())
            await recipient.send(embed=message)
