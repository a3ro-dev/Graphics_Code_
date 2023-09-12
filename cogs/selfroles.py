import discord
from discord.ext import commands
from discord import Embed, app_commands
from discord.ui import View, Button
from selenium.webdriver.common.actions import interaction

import config as cfg

ping_roles_description = """
<a:_:932299160881885205> <a:announcement:1151139265850396712> <@&992656872974852146> 
<a:_:994538693807317002> <a:partnership:1151139524232097904> <@&992657042751889458> 
<a:_:994525998324392006> <a:giveaway:1151139604271992925> <@&992657167901544468> 
<a:_:936620457648603186> <a:evento:1151139687566676010> <@&992657416653131796> 
"""

age_roles_description = """
<:_:940174397224923206> <a:_:1151140903172460575> <@&994527158875725846>
<:_:940174349187575809> <a:_:1151140927742672947> <@&994527154761105438> 
"""

gender_roles_description = """
<a:_:942070637927759932> <a:male:1151141709808414763> <@&994527162952597554> 
<a:_:942070713987260426> <a:female:1151141787419803759> <@&994527166907818054>
"""

class PING_BUTTONS(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Announcement', style=discord.ButtonStyle.red, custom_id="button:Announcement",emoji="<a:announcement:1151139265850396712>" )
    async def selfrannouncement(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(992656872974852146)
        user = interaction.user
        if role in user.roles:
            await user.remove_roles(role)
            embed=Embed(description=f"{role.mention} was removed from you.", color=cfg.CLR)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        elif role not in user.roles:
            await user.add_roles(role)
            embed=Embed(description=f"{role.mention} was added to you.", color=cfg.CLR)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
    @discord.ui.button(label='Partnership', style=discord.ButtonStyle.red, custom_id="button:partnership",emoji="<a:partnership:1151139524232097904>" )
    async def selfrpartnership(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(992657042751889458)
        user = interaction.user
        if role in user.roles:
            await user.remove_roles(role)
            embed=Embed(description=f"{role.mention} was removed from you.", color=cfg.CLR)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        elif role not in user.roles:
            await user.add_roles(role)
            embed=Embed(description=f"{role.mention} was added to you.", color=cfg.CLR)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
    @discord.ui.button(label='Giveaway', style=discord.ButtonStyle.red, custom_id="button:Giveaway",emoji="<a:giveaway:1151139604271992925>" )
    async def selfrGiveaway(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(992657167901544468)
        user = interaction.user
        if role in user.roles:
            await user.remove_roles(role)
            embed=Embed(description=f"{role.mention} was removed from you.", color=cfg.CLR)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        elif role not in user.roles:
            await user.add_roles(role)
            embed=Embed(description=f"{role.mention} was added to you.", color=cfg.CLR)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

    @discord.ui.button(label='Event', style=discord.ButtonStyle.red, custom_id="button:event",emoji="<a:evento:1151139687566676010>" )
    async def selfrevent(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(992657416653131796)
        user = interaction.user
        if role in user.roles:
            await user.remove_roles(role)
            embed=Embed(description=f"{role.mention} was removed from you.", color=cfg.CLR)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        elif role not in user.roles:
            await user.add_roles(role)
            embed=Embed(description=f"{role.mention} was added to you.", color=cfg.CLR)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

class GENDER_BUTTONS(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Male', style=discord.ButtonStyle.red, custom_id="button:Male",emoji="<a:male:1151141709808414763>" )
    async def selfrMale(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(994527162952597554)
        user = interaction.user
        if role in user.roles:
            await user.remove_roles(role)
            embed=Embed(description=f"{role.mention} was removed from you.", color=cfg.CLR)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        elif role not in user.roles:
            await user.add_roles(role)
            embed=Embed(description=f"{role.mention} was added to you.", color=cfg.CLR)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

    @discord.ui.button(label='Female', style=discord.ButtonStyle.red, custom_id="button:Female",emoji="<a:female:1151141787419803759>")
    async def selfrFemale(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(994527166907818054)
        user = interaction.user
        if role in user.roles:
            await user.remove_roles(role)
            embed=Embed(description=f"{role.mention} was removed from you.", color=cfg.CLR)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        elif role not in user.roles:
            await user.add_roles(role)
            embed=Embed(description=f"{role.mention} was added to you.", color=cfg.CLR)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

class AGE_BUTTONS(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='-18', style=discord.ButtonStyle.red, custom_id="button:-18",emoji="<a:_:1151140903172460575>" )
    async def selfr_18(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(994527158875725846)
        user = interaction.user
        if role in user.roles:
            await user.remove_roles(role)
            embed=Embed(description=f"{role.mention} was removed from you.", color=cfg.CLR)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        elif role not in user.roles:
            await user.add_roles(role)
            embed=Embed(description=f"{role.mention} was added to you.", color=cfg.CLR)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

    @discord.ui.button(label='18', style=discord.ButtonStyle.red, custom_id="button:18",emoji="<a:_:1151140927742672947>" )
    async def selfr18(self, interaction: discord.Interaction, button: discord.ui.Button):
        role = interaction.guild.get_role(994527154761105438)
        user = interaction.user
        if role in user.roles:
            await user.remove_roles(role)
            embed=Embed(description=f"{role.mention} was removed from you.", color=cfg.CLR)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        elif role not in user.roles:
            await user.add_roles(role)
            embed=Embed(description=f"{role.mention} was added to you.", color=cfg.CLR)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

class selfroles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.bot.add_view(PING_BUTTONS())
        self.bot.add_view(AGE_BUTTONS())
        self.bot.add_view(GENDER_BUTTONS())

    @app_commands.command()
    @app_commands.default_permissions(administrator=True)
    async def selfroles(self, interaction: discord.Interaction):
        await interaction.response.send_message("Self-Roles sent!", ephemeral=True)
        embed1 = Embed(color=cfg.CLR)
        embed1.title = "<a:_:941690462081810442><a:_:957552706103418920>**__PING ROLES__**<a:_:941690462081810442><a:_:957552706103418920> ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ"
        embed1.description = ping_roles_description

        embed3 = Embed(color=cfg.CLR)
        embed3.title = "## __GENDER ROLES__"
        embed3.description = gender_roles_description

        embed4 = Embed(color=cfg.CLR)
        embed4.title = "## __AGE ROLES__"
        embed4.description = age_roles_description

        await interaction.channel.send(embed=embed1, view=PING_BUTTONS())
        await interaction.channel.send(embed=embed3, view=GENDER_BUTTONS())
        await interaction.channel.send(embed=embed4, view=AGE_BUTTONS())



async def setup(bot):
    await bot.add_cog(selfroles(bot))

# class PING_Dropdown(discord.ui.Select):
#     def __init__(self):
#         options = [
#             discord.SelectOption(label='Announcement', description=f'Get this role', emoji='<a:_:932299160881885205>'),
#             discord.SelectOption(label='Giveaway', description='Get this role', emoji='<a:_:994538693807317002>'),
#             discord.SelectOption(label='Event', description='Get this role', emoji='<a:_:994525998324392006>'),
#             discord.SelectOption(label='Partnership', description='Get this role', emoji='<a:_:936620457648603186>'),
#         ]
#
#         super().__init__(placeholder='Choose your roles...', min_values=1, max_values=4, options=options)
#
#     async def callback(self, interaction: discord.Interaction):
#
#         if self.values[0] == "Announcement":
#             role = interaction.guild.get_role(992656872974852146)
#             user = interaction.user
#             if role in user.roles:
#                         await user.remove_roles(role)
#                         embed=Embed(description=f"{role.mention} was removed from you.", color=cfg.CLR)
#                         await interaction.response.send_message(embed=embed, ephemeral=True)
#                         return
#             elif role not in user.roles:
#                 await user.add_roles(role)
#                 embed=Embed(description=f"{role.mention} was added to you.", color=cfg.CLR)
#                 await interaction.response.send_message(embed=embed, ephemeral=True)
#                 return
#
#         if self.values[0] == "Giveaway":
#             role = interaction.guild.get_role(992657167901544468)
#             user = interaction.user
#             if role in user.roles:
#                         await user.remove_roles(role)
#                         embed=Embed(description=f"{role.mention} was removed from you.", color=cfg.CLR)
#                         await interaction.response.send_message(embed=embed, ephemeral=True)
#                         return
#             elif role not in user.roles:
#                 await user.add_roles(role)
#                 embed=Embed(description=f"{role.mention} was added to you.", color=cfg.CLR)
#                 await interaction.response.send_message(embed=embed, ephemeral=True)
#                 return
#
#         if self.values[0] == "Event":
#             role = interaction.guild.get_role(992657042751889458)
#             user = interaction.user
#             if role in user.roles:
#                         await user.remove_roles(role)
#                         embed=Embed(description=f"{role.mention} was removed from you.", color=cfg.CLR)
#                         await interaction.response.send_message(embed=embed, ephemeral=True)
#                         return
#             elif role not in user.roles:
#                 await user.add_roles(role)
#                 embed=Embed(description=f"{role.mention} was added to you.", color=cfg.CLR)
#                 await interaction.response.send_message(embed=embed, ephemeral=True)
#                 return
#
#         if self.values[0] == "Partnership":
#             role = interaction.guild.get_role(992657416653131796)
#             user = interaction.user
#             if role in user.roles:
#                         await user.remove_roles(role)
#                         embed=Embed(description=f"{role.mention} was removed from you.", color=cfg.CLR)
#                         await interaction.response.send_message(embed=embed, ephemeral=True)
#                         return
#             elif role not in user.roles:
#                 await user.add_roles(role)
#                 embed=Embed(description=f"{role.mention} was added to you.", color=cfg.CLR)
#                 await interaction.response.send_message(embed=embed, ephemeral=True)
#                 return
