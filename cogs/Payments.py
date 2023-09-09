import discord
from discord.ext import commands
from discord.ui import View, Button
from discord import Embed
import config as cfg
from discord import app_commands


class PaymentButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='INR', style=discord.ButtonStyle.grey, custom_id="button:INR", emoji = "<:_:1033684955173224470>")
    async def INR_BUTTON(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Select your payment method", color=cfg.CLR)
        embed.description = "Select your payment method"
        await interaction.response.send_message(embed=embed, view=INRButtons(), ephemeral=True)

    @discord.ui.button(label='USD', style=discord.ButtonStyle.grey, custom_id="button:USD", emoji = "<:_:1033684950228148244>")
    async def USD_BUTTON(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Select your payment method", color=cfg.CLR)
        embed.description = "Select your payment method"
        await interaction.response.send_message(embed=embed, view=USDButtons(), ephemeral=True)


class INRButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='PAYTM', style=discord.ButtonStyle.grey, custom_id="button:PAYTM", emoji = '<:_:1026413314386968616>')
    async def PAYTM_BUTTON(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="PAYTM QR CODE", color=cfg.CLR)
        embed.set_footer(icon_url=interaction.guild.icon, text="SCAN ME")
        embed.set_image(
            url=cfg.PAYTMQR)
        PaytmLinkButton = Button(label='Paytm Link', url=cfg.PAYTMLINK,
                                 emoji='<:_:1026413314386968616>')

        view = View()
        view.add_item(PaytmLinkButton)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


    @discord.ui.button(label='GOOGLE PAY', style=discord.ButtonStyle.grey, custom_id="button:GPAY", emoji="<:_:1019265091369193603>")
    async def GPAY_BUTTON(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="PAYTM QR CODE", color=cfg.CLR)
        embed.set_footer(icon_url=interaction.guild.icon, text="SCAN ME")
        embed.set_image(
            url=cfg.GPAYQR)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label='UPI', style=discord.ButtonStyle.grey, custom_id="button:UPI", emoji = "<:_:1024330100616986784>")
    async def UPI_BUTTON(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="Select your payment method", color=cfg.CLR)
        embed.description = "Select your payment method"
        await interaction.response.send_message(embed=embed, view=UPI(), ephemeral=True)

class USDButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='PAYPAL', style=discord.ButtonStyle.grey, custom_id="button:PAYPAL",
                       emoji="<:_:1019265189465554974>")
    async def PAYPAL_BUTTON(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="PAYPAL LINK", color=cfg.CLR)
        embed.set_footer(icon_url=interaction.guild.icon, text="Pay using PayPal")
        PAYPALLinkButton = Button(label='PAYPAL LINK ', url=cfg.PAYPAL,
                                  emoji='<:_:1019265189465554974>')

        view = View()
        view.add_item(PAYPALLinkButton)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class UPI(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='UPI 1', style=discord.ButtonStyle.grey, custom_id="button:FAMPAYCCHEM",emoji="<:_:1024330100616986784>" )
    async def FAMPAYCHEM(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="UPI QR CODE", color=cfg.CLR)
        embed.set_footer(icon_url=interaction.guild.icon, text="SCAN ME")
        embed.set_image(
            url=cfg.FAMPAYCHEM)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label='UPI 2', style=discord.ButtonStyle.grey, custom_id="button:FAMPAYAERO", emoji="<:_:1024330100616986784>")
    async def FAMPAYAERO(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title="UPI QR CODE", color=cfg.CLR)
        embed.set_footer(icon_url=interaction.guild.icon, text="SCAN ME")
        embed.set_image(
            url=cfg.FAMPAYAERO)
        await interaction.response.send_message(embed=embed, ephemeral=True)

class Payments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="This bot command send the payment information")
    async def payment(self, interaction: discord.Interaction, ):
        embed = Embed(title="Payment Panel")
        embed.description = 'Choose the most suitable payment method'
        embed.color = cfg.CLR
        await interaction.response.send_message(embed=embed, view=PaymentButtons(), ephemeral=True)

async def setup(bot):
    await bot.add_cog(Payments(bot))





