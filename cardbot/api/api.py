"""Contains generic types used by all API implementations to return back to the Discord handlers."""
from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional, Tuple


class SearchResult:
    """Class representing the result of a card search."""

    def __init__(self, name: str = "", set_name: str = "", set_no: int = 0,
                 set_max: int = 0, release: date = date.today(), card_id: str = "") -> None:
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

    def __init__(self, name: str = "", supertype: str = "", subtype: str = "",
                 legality: str = "", set_name: str = "", set_no: int = 0,
                 set_max: int = 0, image: str = "", set_icon: str = "",
                 fields: List[Tuple[str, str]] = [], hp: Optional[int] = None,
                 evolves_from: Optional[str] = None, types: Optional[List[str]] = None) -> None:
        """
        Construct a ShowResult.

        :param name: The name of the card
        :param supertype: The supertype of the card (e.g. Pokémon, Trainer)
        :param subtype: The subtype of the card (e.g. Basic, Tool)
        :param legality: The most restrictive format the card is legal in (e.g. Standard)
        :param set_name: The name of the set the card is in
        :param set_no: The card's number within the set
        :param set_max: The maximum count of cards within the set
        :param image: The URL to the card's image
        :param set_icon: The URL to the image of the icon of the set the card is from
        :param fields: List of fields to add in the form of (title, content)
        :param hp: The Pokemon's HP, if any
        :param evolves_from: The Pokemon this card evolves from, if any
        :param types: The card's types, if any
        """
        self.name = name
        self.supertype = supertype
        self.subtype = subtype
        self.legality = legality
        self.set_name = set_name
        self.set_no = set_no
        self.set_max = set_max
        self.image = image
        self.set_icon = set_icon
        self.fields = fields
        self.hp = hp
        self.evolves_from = evolves_from
        self.types = types


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
