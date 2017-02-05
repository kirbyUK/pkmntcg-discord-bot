# pkmntcg-discord-bot

Discord bot for a Pokemon TCG server. Can search cards and display the text and
a link to the image. Uses [discord.py](https://discordpy.readthedocs.io/en/latest/)
for the Discord API and [pokemontcg.io](https://pokemontcg.io/) for the cards.

The bot can be seen used on the following Discord server: https://discord.gg/UgfcThp

![sample usage](https://raw.githubusercontent.com/kirbyUK/pkmntcg-discord-bot/master/preview.png)

## Installation

This needs working on but currently the following will install what is needed.

```
git clone https://github.com/kirbyUK/pkmntcg-discord-bot
cd pkmntcg-discord-bot
pip install -r requirements.txt
```

You then need to register a new bot from your Discord developer account and place
the token in the root directory of the repository in a file called `token`. With
that in place simply run:

```
cd cardbot
python3 cardbot.py
```

## Usage

From the bot's own output, using the `!help` command:

```
!search [card-name]
    Gives a list of all cards matching the search
    [card-name], as well as the set code and name.

    e.g.
        !search ambipom
        !search ninja boy
        !search splash energy

!show [card-name] [set-code]
    Displays the text and image of the given card
    from the given set. If you are unsure of the
    set code, find it using !search first.

    e.g.
        !show ambipom xy11-91
        !show ninja boy xy11-103
        !show splash energy xy9-113
```
