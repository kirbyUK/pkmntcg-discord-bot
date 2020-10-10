"""Module containing Discord command implementing functions."""
from functools import lru_cache

import discord

from cardbot.api.pokemontcgio_v1 import PokemonTCGIOV1Provider


def cardbot_search(search_term: str) -> discord.Embed:
    """
    Search for cards with the given search term.

    :param search_term: The search term to pass to the API
    :returns: The Discord embed to send back as a result of the command
    """
    results = PokemonTCGIOV1Provider().search(search_term)
    if len(results) == 0:
        # Give back an error if there were no search results
        embed = discord.Embed(
            title=f":warning: No matches for search '{search_term}'",
            color=0xff0000)
    elif len(results) == 1:
        # If there was exactly one result, save the user some time and give
        # the card embed object instead
        embed = cardbot_show(results[0].id)
    else:
        # Otherwise, give back an embed showing the available results
        embed = discord.Embed(title=f"Matches for search '{search_term}'")
        embed.add_field(
            name="\u200b",
            value="\n".join([f"{r.name} - {r.set} {r.set_no}/{r.set_max} (`{r.id}`)"
                             for r in results])
        )

    return embed


@lru_cache(maxsize=1024)
def cardbot_show(card_id: str) -> discord.Embed:
    """
    Construct a Discord embed for a given Pokemon card.

    :param card_id: The card to construct a Discord embed for
    :returns: The constructed Discord embed object for the card
    """
    return discord.Embed(title="tbd")


def cardbot_help() -> discord.Embed:
    """
    Get usage on the bot commands.

    :returns: Instructions for using the bot
    """
    embed = discord.Embed(title="Cardbot Help")
    embed.add_field(
        name="!search [card-name]",
        value="""
Gives a list of all cards matching the search, as well as the set code and name.

e.g.
    `!search ambipom`
    `!search ninja boy`
    `!search splash energy`
""")
    embed.add_field(
        name="!show [set-code]",
        value="""
Displays the text and image of the given card from the given set. If you are unsure of the set code, find it using !search first.

e.g.
    `!show xy11-91`
    `!show xy11-103`
    `!show xy9-113`
""")
    embed.set_footer(text="Source: https://github.com/kirbyUK/pkmntcg-discord-bot")
    return embed
