#!/usr/bin/env python3
from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype

def search(name):
	# Search for the given text
	cards = Card.where(name = name).all()

	if name == "":
		return

	# Give an error if there are no matches
	if len(cards) == 0:
		return "No matches for search '%s'" % name

	# If there are matches, build a string with the name, set and set code
	# of every match
	cards_with_sets = []
	for card in cards:
		card_set = Set.find(card.set_code)

		# Re-arrange the release data so it is ISO
		date_split = card_set.release_date.split("/")
		card_set.release_date = ("%s-%s-%s" %
			(date_split[2], date_split[0], date_split[1]))

		cards_with_sets.append((card, card_set))

	# Sort the list of cards by set release date
	cards_with_sets.sort(key = lambda card : card[1].release_date)

	# Create the returned string
	return_str = "Matches for search '%s'\n" % name
	for card in cards_with_sets:
		return_str += ("%s - %s %s/%s (`%s`)\n" %
			(card[0].name, card[1].name, card[0].number, card[1].total_cards, card[1].code))
	return return_str
