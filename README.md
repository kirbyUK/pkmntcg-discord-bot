# pkmntcg-discord-bot

Discord bot for a Pokemon TCG server. Can search cards and display the text and
a link to the image. Uses [discord.py](https://discordpy.readthedocs.io/en/latest/)
for the Discord API and [pokemontcg.io](https://pokemontcg.io/) for the cards.

The bot can be seen used on the following Discord server: https://discord.gg/UgfcThp

![sample usage](https://raw.githubusercontent.com/kirbyUK/pkmntcg-discord-bot/master/preview.png)

## Installation

Simply clone the directory, install dependencies then run the setup script

```
git clone https://github.com/kirbyUK/pkmntcg-discord-bot
cd pkmntcg-discord-bot
make init
python setup.py build
python setup.py install
```

You then need to register a new bot from your Discord developer account and get
a token for the bot, as well as invite it to any channels desired. Once a token
is obtained, you can supply it as a command line argument or place it in a file.
Running the bot using both these methods is shown here:

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
```
