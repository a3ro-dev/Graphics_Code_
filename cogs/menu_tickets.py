import discord
from discord.ext import commands
import config as cfg
import asyncio
import time

class Tickets(commands.Cog):
    """
    This Is The Main Class For Ticket Related Commands
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.add_view(TicketView())
        self.bot.add_view(Close())

    @commands.hybrid_command(aliases=['tick', 'ticket', 'support'])
    @commands.has_permissions(administrator=True)
    async def open_ticket(self, ctx: commands.Context):
        try:
            await ctx.send(content="Please select a ticket type", view=TicketView())
        except Exception as e:
            print(f"Failed to open ticket: {e}")

class Tickett(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Designer Application", description="Apply as the creative staff at Graphics Code 2.0", value="Designer Application"),
            discord.SelectOption(label="Staff Application", description="Apply as a staff at Graphics Code 2.0", value="Staff Application"),
            discord.SelectOption(label="Partnership Application", description="Partner with us", value="Partnership")
        ]

        super().__init__(placeholder='Choose a type of ticket...', min_values=1, max_values=1, custom_id="Tick:panel",
                         options=options)

    async def callback(self, interaction: discord.Interaction):
        try:
            if self.values[0] == "Designer Application":
                mod = interaction.guild.get_role(cfg.SUPPORT) #type: ignore
                categ = discord.utils.get(interaction.guild.categories, id=cfg.DESIGNER_APP) #type: ignore
                await interaction.response.send_message("Creating a ticket for you, this may take a while!", ephemeral=True)
                ticket_channel = await categ.create_text_channel(name=f"order-{interaction.user.name}") #type: ignore

                await ticket_channel.set_permissions(interaction.user, view_channel=True, send_messages=True) #type: ignore
                await ticket_channel.set_permissions(mod, read_messages=True, send_messages=True) #type: ignore
                view = Close()
                await ticket_channel.send(
                        f"{interaction.user.mention} | <@&{cfg.SUPPORT}> ")
                embed = discord.Embed(title=f"{interaction.guild.name} Support!", #type: ignore
                                      description="Thank you for reaching out. Our creative staff will see to your application soon.")
                await ticket_channel.send(embed=embed, view=view)

            if self.values[0] == "Staff Application":
                admin = interaction.guild.get_role(cfg.SUPPORT) #type: ignore
                categ = discord.utils.get(interaction.guild.categories, id=cfg.STAFF_APP) #type: ignore
                await interaction.response.send_message("Creating a ticket for you, this may take a while!", ephemeral=True) 
                ticket_channel = await categ.create_text_channel(name=f"issue-{interaction.user.name}") #type: ignore

                await ticket_channel.set_permissions(interaction.user, view_channel=True, send_messages=True) #type: ignore
                await ticket_channel.set_permissions(admin, read_messages=True, send_messages=True) #type: ignore
                view = Close()
                await ticket_channel.send(
                        f"{interaction.user.mention} | <@&{cfg.SUPPORT}> ")
                embed = discord.Embed(title=f"{interaction.guild.name} Support!", #type: ignore
                                      description="Thank you for reaching out. The staff will see to your application soon.")
                await ticket_channel.send(embed=embed, view=view)
            
            if self.values[0] == "Partnership":
                partnershipmod = interaction.guild.get_role(cfg.PARTNERSHIP_MANAGER)  #type: ignore
                categ = discord.utils.get(interaction.guild.categories, id=cfg.PARTNERSHIP_APP) #type: ignore
                await interaction.response.send_message("Creating a ticket for you, this may take a while!", ephemeral=True)
                ticket_channel = await categ.create_text_channel(name=f"partnership-{interaction.user.name}") #type: ignore

                await ticket_channel.set_permissions(interaction.user, view_channel=True, send_messages=True) #type: ignore
                await ticket_channel.set_permissions(partnershipmod, read_messages=True, send_messages=True) #type: ignore
                view = Close()
                await ticket_channel.send(
                        f"{interaction.user.mention} | <@&{cfg.PARTNERSHIP_MANAGER}> ")
                embed = discord.Embed(title=f"{interaction.guild.name} Support!", #type: ignore
                                      description="Thank you for reaching out. Our partnership manager will assist you with your partnership inquiry.")
                await ticket_channel.send(embed=embed, view=view)
        except Exception as e:
            print(e)
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Tickett())

class Close(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @discord.ui.button(label='CLOSE', style=discord.ButtonStyle.danger, custom_id='CLOSE:RED')
    async def closeticket(self, interaction=discord.Interaction, button=discord.ui.Button, ):
        await interaction.channel.send(f'This ticket was closed by {interaction.user.mention}')
        channel = interaction.channel
        time.sleep(10)
        await channel.delete()

async def setup(bot: commands.Bot):
    try:
        await bot.add_cog(Tickets(bot))
        print("Tickets cog loaded successfully")
    except Exception as e:
        print(f"Failed to load Tickets cog: {e}")
