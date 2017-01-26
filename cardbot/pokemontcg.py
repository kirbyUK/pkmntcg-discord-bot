#!/usr/bin/env python3
from pokemontcgsdk import Card
from pokemontcgsdk import Set
from pokemontcgsdk import Type
from pokemontcgsdk import Supertype
from pokemontcgsdk import Subtype

# Shorthand symbols for attack energy costs, as used by PokeBeach
short_energy = {
	"Colorless" : "[C]",
	"Darkness" :  "[D]",
	"Fairy" :     "[Y]",
	"Fighting" :  "[F]",
	"Fire" :      "[R]",
	"Grass" :     "[G]",
	"Lightning" : "[L]",
	"Leaf" :      "[G]",
	"Metal" :     "[M]",
	"Psychic" :   "[P]",
	"Water" :     "[W]",
}

# Given a string, searches for cards by name using the given string. Return a
# list of matches sorted by release, and the set name and code the card was
# released in
def search(name):
	# Search for the given text
	cards = Card.where(name = name).all()

	if name == "":
		return

	# Give an error if there are no matches
	if len(cards) == 0:
		return "No matches for search '%s'" % name

	# If there is exactly one match, save time for the user and give the
	# !show output instead
	if len(cards) == 1:
		return show(cards[0].name, cards[0].set_code)

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
			(card[0].name, card[1].name, card[0].number,
			 card[1].total_cards, card[1].code))
	return return_str

# Given a card name and set code, display an image and the text of the card
def show(name, card_set):
	# Search for the given card
	cards = Card.where(name = name).where(setCode=card_set).all()

	if len(cards) == 0:
		return ("No results found for '%s' in set `%s`" %
			(name, card_set))

	if len(cards) > 1:
		return "Too many results"

	card = cards[0]

	# Create a string for the card text
	return_str = "%s\n" % card.image_url
	return_str += "```\n"

	# Pokemon are the most involved as they have a lot going on
	if card.supertype == "Pokémon":
		return_str += "%s - %s - HP%s\n" % (card.name, "/".join(card.types), card.hp)
		return_str += "%s Pokemon\n\n" % card.subtype
		if card.ability != None:
			return_str += "%s: %s\n" % (card.ability['type'], card.ability['name'])
			return_str += "%s\n" % card.ability['text']
			return_str += "\n"
		if card.attacks != None:
			for attack in card.attacks:
				for cost in attack['cost']:
					return_str += "%s" % short_energy[cost]
				return_str += " %s" % attack['name']
				if attack['damage'] != '':
					return_str += ": %s damage\n" % attack['damage']
				else:
					return_str += "\n"
				if attack['text'] != None:
					return_str += "%s\n" % attack['text']
				return_str += "\n"
		if card.weaknesses != None:
			for weakness in card.weaknesses:
				return_str += ("Weakness: %s (%s)\n" %
					(weakness['type'], weakness['value']))
		if card.resistances != None:
			print(card.resistances)
			for resistance in card.resistances:
				return_str += ("Resistance: %s (%s)\n" %
					(resistance['type'], resistance['value']))
		return_str += "Retreat: %s" % len(card.retreat_cost)

	# Trainers and Energy are a lot easier
	elif card.supertype == "Trainer" or card.supertype == "Energy":
		return_str += "%s\n" % card.name
		return_str += "%s\n\n" % card.subtype
		return_str += "%s\n" % card.text[0]

	return_str += "```\n"
	return return_str
