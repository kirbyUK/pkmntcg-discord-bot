"""Module containing Discord command implementing functions."""
from functools import lru_cache

import discord

from cardbot.api.pokemontcgio_v1 import PokemonTCGIOV1Provider
from cardbot.emoji import colours, emoji


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
    card = PokemonTCGIOV1Provider().show(card_id)
    if card:
        # Constructing the title, description and colours of embeds differs depending
        # on if the card is a Pokemon or not
        if card.supertype == "Pokémon":
            # The title contains the Pokemon's name, HP and types
            title = card.name
            if card.hp:
                title += f" - HP{card.hp}"
            if card.types:
                title += f" - {'/'.join([emoji[x] for x in card.types])}"

            # The description contains the card's subtype, and evolution (if any)
            desc = f"{card.subtype} Pokémon"
            if card.evolves_from and card.evolves_from != "":
                desc += f" (Evolves from {card.evolves_from})"

            # The colour is based on the Pokemon's type
            if card.types and len(card.types) > 0:
                colour = colours[card.types[0]]
            else:
                colour = 0x969696

            embed = discord.Embed(title=title, description=desc, color=colour)
        else:
            embed = discord.Embed(title=card.name, description=card.subtype)

        # Adding fields, the card image and the footer are common across all card types
        for field in card.fields:
            embed.add_field(name=field[0], value=field[1], inline=False)
        embed.set_image(url=card.image)
        embed.set_footer(
            text=f"{card.set_name} - {card.set_no}/{card.set_max} ({card.legality})",
            icon_url=card.set_icon)
    else:
        embed = discord.Embed(title=f":warning: No card with id '{card_id}'", color=0xff0000)

    return embed


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
