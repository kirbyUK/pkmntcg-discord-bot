# pkmntcg-discord-bot

**As of 2022-03-28, this project is DEPRECATED. There has been a new version of
  the Pokemon TCG API for a while, and I think there's changes coming to
  discord.py that I'm not going to implement either.**

Discord bot for a Pokemon TCG server. Can search cards and display the text and
a link to the image. Uses [discord.py](https://discordpy.readthedocs.io/en/latest/)
for the Discord API and [pokemontcg.io](https://pokemontcg.io/) for the cards.

![sample usage](https://raw.githubusercontent.com/kirbyUK/pkmntcg-discord-bot/master/preview.png)

## Installation

```sh
git clone https://github.com/kirbyUK/pkmntcg-discord-bot
cd pkmntcg-discord-bot
python -m venv venv
pip install .
```

You then need to [register a new bot](https://discordapp.com/developers/applications/me)
from your Discord developer account and get a token for the bot, as well as
invite it to any channels desired. Once a you have the token,  you can supply
it as a command line argument or place it in a file. Running the bot using both
these methods is shown here:

```
cardbot -t [YOUR-TOKEN-HERE]
cardbot -f /path/to/token/file
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

!show [set-code]
    Displays the text and image of the given card
    from the given set. If you are unsure of the
    set code, find it using !search first.

    e.g.
        !show xy11-91
        !show xy11-103
        !show xy9-113

!text [set-code]
    Similar to !show, however gives just the card text
    in a copy-and-pastable format.

    e.g.
        !text xy11-91
        !text xy11-103
        !text xy9-113
```
