import aiosqlite
import discord
import discord.utils
from discord.ext import commands

import config as cfg


async def modal_helper(value, art):
    db = await aiosqlite.connect('/home/ubuntu/graphics-code-bott/db/points.db')
    cursor = await db.cursor()
    await cursor.execute("SELECT * FROM points WHERE user_id = ?", (art,))
    try:
        res = await cursor.fetchone()
        if value.lower() == "vfx":
            points = res[1] + 2
        elif value.lower() == "gfx":
            points = res[1] + 1
        else:
            return ValueError
        await cursor.execute("UPDATE points SET points = ? WHERE user_id = ?", (points, art))
        await db.commit()

    except TypeError:
        if value.lower() == "vfx":
            points = 2
        elif value.lower() == "gfx":
            points = 1
        else:
            return ValueError

        await cursor.execute("INSERT INTO points (user_id, points) VALUES (?, ?)", (art, points))
        await db.commit()


class Modals(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.add_view(OrderingModalViewBut())

    @commands.command(aliases=['order', 'form', 'fxform'])
    @commands.has_permissions(administrator=True)
    async def orderform(self, ctx):
        embed = discord.Embed(title="Order form",
                              description="**Fill The Form**",
                              color=cfg.CLR)
        embed.set_image(url="https://media.discordapp.net/attachments/992660600746422312/1026378406264307732/form.gif")
        view = OrderingModalViewBut()
        await ctx.send(embed=embed, view=view)


class OrderingCallModalView(discord.ui.Modal, title='Fill me'):
    q1 = discord.ui.TextInput(
        label='What are you ordering?',
        style=discord.TextStyle.short,
        placeholder='Order Type',
        required=True,
        max_length=200
    )

    q2 = discord.ui.TextInput(
        label='Colour theme',
        style=discord.TextStyle.short,
        placeholder='Color Scheme',
        required=True,
        max_length=500
    )

    q3 = discord.ui.TextInput(
        label='Example of what you are ordering',
        style=discord.TextStyle.short,
        placeholder='link suggested',
        required=True,
        max_length=300
    )

    q4 = discord.ui.TextInput(
        label='Payment Method',
        style=discord.TextStyle.short,
        placeholder='Paytm, Bank, Paypal, Upi, etc..',
        required=True,
        max_length=200
    )
    q5 = discord.ui.TextInput(
        label='Deadline',
        style=discord.TextStyle.short,
        placeholder='Minimum 3 days should be given',
        required=False,
        max_length=500
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        embed = discord.Embed(color=cfg.CLR)
        embed.title = f'Order form - __{interaction.user.name}__'
        embed.add_field(name='What are you ordering?', value=f'`{self.q1.value}`', inline=True)
        embed.add_field(name='Colour theme', value=f'`{self.q2.value}`', inline=False)
        embed.add_field(name='Example of what you are ordering', value=f'`{self.q3.value}`', inline=False)
        embed.add_field(name='Payment Method', value=f'`{self.q4.value}`', inline=True)
        embed.add_field(name='Deadline', value=f'`{self.q5.value}`', inline=True)
        embed.set_thumbnail(url=interaction.guild.icon.url)
        embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon)
        await interaction.followup.send(embed=embed)


class OrderingModalViewBut(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='<:graphicscode:985936754446073958>', style=discord.ButtonStyle.gray, custom_id='applybut')
    async def callmodalcallback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(OrderingCallModalView())


async def setup(bot):
    await bot.add_cog(Modals(bot))
