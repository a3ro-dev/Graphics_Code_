import os
import discord
from discord.ext import commands
import config as cfg
from cogs.points import LBV
import aiosqlite

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(case_insensitive=True, command_prefix=commands.when_mentioned_or(cfg.PREFIX), intents=intents,
                         owner_ids=[905658967005495356])  # help_command=None,
        
    async def connect_database(self):
        self.db = await aiosqlite.connect('/home/ubuntu/graphics-code-bott/db/points.db')
    async def setup_hook(self) -> None:
        
        self.add_view(LBV(self.db))


bot = Bot()


@bot.event
async def on_ready():
    print(f'--------------------------------------------------------------')
    print(f'Logged in as {bot.user.name} | {bot.user.id}')
    print(f'--------------------------------------------------------------')
    await bot.load_extension(f'jishaku')

    print(f'--------------------------------------------------------------')
    print("🔴🔴🔴🔴 Now loading cogs! 🔴🔴🔴🔴")
    print(f'--------------------------------------------------------------')
    for file in os.listdir('./cogs'):
        if file.endswith('.py'):
            try:
                await bot.load_extension(f'cogs.{file[:-3]}')
                print(f' | ✅ | loaded {file[:-3]}')
            except Exception as e:
                print(f' | ❌ | Failed to load {file[:-3]} because: {str(e)}')

    print(f'--------------------------------------------------------------')
    print("🔴🔴🔴🔴 Now loading Tickets! 🔴🔴🔴🔴")
    print(f'--------------------------------------------------------------')
    for file in os.listdir('./TicketSystems'):
        if file.endswith('.py'):
            try:
                await bot.load_extension(f'TicketSystems.{file[:-3]}')
                print(f' | ✅ | loaded {file[:-3]}')
            except Exception as e:
                print(f' | ❌ | Failed to load {file[:-3]} because: {str(e)}')

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.streaming, name='graphiccodes.xyz',
                                                        url='https://www.twitch.tv/search?term=graphicscode'))


bot.run(cfg.TOKEN)
