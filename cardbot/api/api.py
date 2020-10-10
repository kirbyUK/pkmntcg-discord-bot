"""Contains generic types used by all API implementations to return back to the Discord handlers."""
from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional


class SearchResult:
    """Class representing the result of a card search."""

    def __init__(self, name: str, set_name: str, set_no: int,
                 set_max: int, release: date, card_id: str) -> None:
        """
        Construct a SearchResult object.

        :param name: The full name of the card
        :param set_name: The full name of the set the card is in
        :param set_no: The card's number within the set
        :param set_max: The maximum number of cards within the set
        :param release: The release date of the set containing the card
        :param card_id: The card's unique ID
        """
        self.name = name
        self.set = set_name
        self.set_no = set_no
        self.set_max = set_max
        self.release = release
        self.id = card_id


class ShowResult:
    """Class representing the result of a card show command."""

    def __init__(self) -> None:
        """Construct a ShowResult."""
        pass


class ApiProvider(ABC):
    """Base class that different API providers must implement."""

    @abstractmethod
    def search(self, search_term: str) -> List[SearchResult]:
        """
        Search the API for cards containing the given string.

        :param search_term: The string to search the cards for
        :returns: The list of search results from the API
        """
        return []

    @abstractmethod
    def show(self, card_id: str) -> Optional[ShowResult]:
        """
        Get details on a specific card.

        :param card_id: The unique ID on the card
        :returns: The result of the card lookup, or None if no card matches
        """
        return None


"""Conversion from type name to emoji."""
emoji = {
    'Colorless': '<:ecolorless:362734594593914890>',
    'Darkness': '<:edarkness:362733180274606080>',
    'Dragon': '<:edragon:362737396179271680>',
    'Fairy': '<:efairy:362733851371503616>',
    'Fighting': '<:efighting:362732793995984917>',
    'Fire': '<:efire:362731242044653578>',
    'Free': '<:ecolorless:362734594593914890>',
    'Grass': '<:egrass:362730672680599552>',
    'Lightning': '<:elightning:362731984474079233>',
    'Psychic': '<:epsychic:362732305359568908>',
    'Metal': '<:emetal:362733507539369984>',
    'Water': '<:ewater:362731629988544512>',
}

"""Conversion from type name to hex colour."""
colour = {
    'Colorless': 0xF5F5DA,
    'Darkness': 0x027798,
    'Dragon': 0xD1A300,
    'Fairy': 0xDD4787,
    'Fighting': 0xC24635,
    'Fire': 0xD7080C,
    'Grass': 0x427B18,
    'Lightning': 0xF9D029,
    'Psychic': 0xB139B6,
    'Metal': 0xAFAFAF,
    'Water': 0x02B2E6,
}
