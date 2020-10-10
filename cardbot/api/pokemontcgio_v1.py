"""Methods for interacting with V1 of the pokemontcg.io API."""
from datetime import date
from typing import List, Optional

from pokemontcgsdk import Card
from pokemontcgsdk import Set

from cardbot.api.api import ApiProvider, SearchResult, ShowResult
from cardbot.emoji import emoji


class PokemonTCGIOV1Provider(ApiProvider):
    """Class that utilises V1 of the pokemontcg.io API to get results."""

    def search(self, search_term: str) -> List[SearchResult]:
        """
        Search the pokemontcg.io API for cards with the given search term.

        :param search_term: The search to give to the API
        :returns: A list of search results given from the search
        """
        # Users will often enter 'hydreigon ex' when they really mean
        # 'hydreigon-ex'. This annoying, but simply inserting the dash does not
        # work as it makes Ruby/Sapphire era ex cards unaccessible. Instead,
        # search for both
        cards = []
        if search_term.lower().endswith(' ex'):
            cards.extend(Card.where(name=search_term.lower()))
            cards.extend(Card.where(name=search_term.lower().replace(' ex', '-ex')))
        # GX cards do not have the same issue, so we can simply insert the dash
        # as expected
        elif search_term.lower().endswith(' gx'):
            cards.extend(Card.where(name=search_term.lower().replace(' gx', '-gx')))
        # Hardcode the card 'N' to search for the specific card, not all cards
        # with the letter n within their name
        elif search_term.lower() == "n":
            cards = Card.where(name="\"N\"")
        # Otherwise, search for the given text
        else:
            cards = Card.where(name=search_term)

        return sorted([PokemonTCGIOV1Provider._card_to_searchresult(card) for card in cards],
                      key=lambda result: result.release)

    def show(self, card_id: str) -> Optional[ShowResult]:
        """
        Get details on a specific card.

        :param card_id: The unique ID on the card
        :returns: The result of the card lookup, or None if no card matches
        """
        card = Card.find(card_id)
        card_set = Set.find(card.set_code)
        if not card:
            return None

        if card.supertype == "Pokémon":
            fields = []

            # If the Pokemon has an ability, it goes in its own field
            if card.ability:
                fields.append((f"{card.ability['type']}: {card.ability['name']}",
                               card.ability["text"] or "\u200b"))

            # Each attack is its own field
            if card.attacks:
                for attack in card.attacks:
                    name = ""
                    text = ""
                    for cost in attack["cost"]:
                        name += emoji[cost]
                    name += f" {attack['name']}"
                    if "damage" in attack and attack["damage"] != "":
                        name += f" - {attack['damage']}"
                    if "text" in attack and attack["text"] != "":
                        text = attack["text"]
                    else:
                        text = "\u200b"
                    fields.append((name, text))

            # Weakness, resistances and retreat all go on the same line
            bottom_line = ""
            if card.weaknesses:
                bottom_line += f"Weakness: "
                bottom_line += ", ".join([f"{emoji[w['type']]} ({w['value']})" for w in card.weaknesses])
            if card.resistances:
                bottom_line += f" - Resistance: "
                bottom_line += ", ".join([f"{emoji[r['type']]} ({r['value']})" for r in card.resistances])
            if card.retreat_cost:
                bottom_line += f" - Retreat: {emoji['Colorless'] * len(card.retreat_cost)}"
            if bottom_line != "":
                fields.append(("\u200b", bottom_line))

            return ShowResult(
                name=card.name,
                supertype=card.supertype,
                subtype=card.subtype,
                legality=PokemonTCGIOV1Provider._newest_legal_format(card),
                set_name=card_set.name,
                set_no=card.number,
                set_max=card_set.total_cards,
                image=card.image_url,
                set_icon=card_set.symbol_url,
                fields=fields,
                hp=card.hp,
                evolves_from=card.evolves_from,
                types=card.types
            )
        else:
            return ShowResult(
                name=card.name,
                supertype=card.supertype,
                subtype=card.subtype,
                legality=PokemonTCGIOV1Provider._newest_legal_format(card),
                set_name=card_set.name,
                set_no=card.number,
                set_max=card_set.total_cards,
                image=card.image_url,
                set_icon=card_set.symbol_url,
                fields=[("\u200b", text) for text in card.text]
            )

    @staticmethod
    def _card_to_searchresult(card: Card) -> SearchResult:
        """
        Convert a pokemontcgsdk Card object to a SearchResult.

        :param card: The card to make a SearchResult from
        :returns: A SearchResult object for the passed Card.
        """
        card_set = Set.find(card.set_code)
        return SearchResult(
            name=card.name,
            set_name=card_set.name,
            set_no=card.number,
            set_max=card_set.total_cards,
            release=PokemonTCGIOV1Provider._set_date_to_date(card_set.release_date),
            card_id=f"{card_set.code}-{card.number}")

    @staticmethod
    def _set_date_to_date(date_str: str) -> date:
        """
        Convert the date of a set given by V1 of the pokemontcg.io API to a Python date object.

        :param date_str: The given set date to convert
        :returns: The given date as a Python date object
        """
        month, day, year = date_str.split("/")
        return date(year=int(year), month=int(month), day=int(day))

    @staticmethod
    def _newest_legal_format(card: Card) -> str:
        """
        Get the most restrictive format the given card is legal in.

        :param card: The card to get the format of
        :returns: The name of the most restrictive format the card is legal in
        """
        card_set = Set.find(card.set_code)
        if card_set.standard_legal:
            legal_format = "Standard"
        elif card_set.expanded_legal:
            legal_format = "Expanded"
        else:
            legal_format = "Legacy"

        return legal_format
