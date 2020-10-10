"""Methods for interacting with V1 of the pokemontcg.io API."""
from datetime import date
from typing import List, Optional

from pokemontcgsdk import Card
from pokemontcgsdk import Set

from cardbot.api.api import ApiProvider, SearchResult, ShowResult


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
        return None

    @staticmethod
    def _card_to_searchresult(card: Card) -> SearchResult:
        """
        Convert a pokemontcgsdk Card object to a SearchResult.

        :param card: The card to make a SearchResult from
        :returns: A SearchResult object for the passed Card.
        """
        card_set = Set.find(card.set_code)
        return SearchResult(
            card.name,
            card_set.name,
            card.number,
            card_set.total_cards,
            PokemonTCGIOV1Provider._set_date_to_date(card_set.release_date),
            f"{card_set.code}-{card.number}")

    @staticmethod
    def _set_date_to_date(date_str: str) -> date:
        """
        Convert the date of a set given by V1 of the pokemontcg.io API to a Python date object.

        :param date_str: The given set date to convert
        :returns: The given date as a Python date object
        """
        month, day, year = date_str.split("/")
        return date(year=int(year), month=int(month), day=int(day))
