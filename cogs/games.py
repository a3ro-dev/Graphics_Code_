import asyncio
import random
from discord.ext import commands
from games import hangman, twenty


class Game(commands.Cog):
    """Play various Games"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='2048')
    async def twenty(self, ctx):
        """Play 2048 game"""
        await twenty.play(ctx, self.bot)

    @commands.command(name='hangman', aliases=['hang'])
    async def hangman(self, ctx):
        """Play Hangman"""
        await hangman.play(self.bot, ctx)

    @commands.command(name='rps', aliases=['rockpaperscissors'])
    async def rps(self, ctx):
        """Play Rock, Paper, Scissors game"""

        def check_win(p, b):
            if p == '🌑':
                return False if b == '📄' else True
            if p == '📄':
                return False if b == '✂' else True
            # p=='✂'
            return False if b == '🌑' else True

        async with ctx.typing():
            reactions = ['🌑', '📄', '✂']
            game_message = await ctx.send("**Rock Paper Scissors**\nChoose your shape:", delete_after=15.0)
            for reaction in reactions:
                await game_message.add_reaction(reaction)
            bot_emoji = random.choice(reactions)

        def check(reaction, user):
            return user != self.bot.user and user == ctx.author and (str(reaction.emoji) == '🌑' or '📄' or '✂')

        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Time's Up! :stopwatch:")
        else:
            await ctx.send(f"**:man_in_tuxedo_tone1:\t{reaction.emoji}\n:robot:\t{bot_emoji}**")
            # if conds
            if str(reaction.emoji) == bot_emoji:
                await ctx.send("**Good Competition, its a tie**")
            elif check_win(str(reaction.emoji), bot_emoji):
                await ctx.send("**Ok..good one..you won. I accept my defeat**")
            else:
                await ctx.send("**I won. Try again next time**")

    @commands.command(name='toss', aliases=['flip'])
    async def toss(self, ctx):
        """Flips a Coin"""
        coin = ['+ heads', '- tails']
        await ctx.send(f"```\n{random.choice(coin)}\n```")

async def setup(bot):
    await bot.add_cog(Game(bot))
