# Graphics Code

## Description

This is a Discord bot project written in Python. It uses the discord.py library and includes various features such as games, custom commands, ticket systems, and more.

## Authors

- Poison
- Adnan(HellTronix)
- Lxghtning
- A3ro-Dev

## Cogs

The bot's functionality is divided into several cogs, each in its own file in the `/cogs` folder:

- [CustomCmds.py](cogs/CustomCmds.py): Contains the code for the custom commands feature.
- [games.py](cogs/games.py): Contains the code for the games feature.
- [help.py](cogs/help.py): Contains the code for the help feature.
- [menu_tickets.py](cogs/menu_tickets.py): Contains the code for the menu tickets feature.
- [Modals.py](cogs/Modals.py): Contains the code for the modals feature.
- [ModMail.py](cogs/ModMail.py): Contains the code for the ModMail feature.
- [music.py](cogs/music.py): Contains the code for the music feature.
- [Payments.py](cogs/Payments.py): Contains the code for the payments feature.
- [points.py](cogs/points.py): Contains the code for the points feature.
- [selfroles.py](cogs/selfroles.py): Contains the code for the self roles feature.
- [tttb.py](cogs/tttb.py): Contains the code for the tttb feature.
- [watermark.py](cogs/watermark.py): Contains the code for the watermark feature.
- [welcome.py](cogs/welcome.py): Contains the code for the welcome feature.

### Orders (FxTicket.py)

This file contains the implementation of the order system in the bot. It's a cog in the discord.py framework, which means it groups related commands, listeners, and other pieces of functionality together.

The `Orders` class handles different types of order commands. It connects to a SQLite database where it presumably stores order information.

The `order_button` command sends an embed message to the Discord channel. This embed contains an ordering panel where users can create an order ticket by clicking one of two buttons for GFX or VFX design. Once a button is clicked, a ticket is automatically created by the bot.

This feature allows for a streamlined and user-friendly way of placing orders directly within Discord.

## Installation

1. Clone this repository.
2. Install the required Python packages using pip:

```sh
pip install -r requirements.txt

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.