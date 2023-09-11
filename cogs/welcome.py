import discord
from discord.ext import commands
from discord.ui import View, Button

import config as cfg


class WELCOME(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_member_join(self, member: discord.Member):
    #     button1 = Button(label='Rules', url="https://discord.com/channels/905665593267609631/905678231896723486",
    #                      emoji='<:Rules:1026538712147972216>')
    #
    #     button2 = Button(label='Self-Roles',
    #                      url="https://discord.com/channels/905665593267609631/992660613790715925",
    #                      emoji='<:self_role:1026674149709590579>')
    #
    #     button3 = Button(label='Store',
    #                      url="https://discord.com/channels/905665593267609631/992660625312460860",
    #                      emoji='<:store:1026538835951231096>')
    #
    #     view = View()
    #     view.add_item(button1)
    #     view.add_item(button2)
    #     view.add_item(button3)
    #     description = (f'{member.mention} just joined the server. We now have {len(member.guild.members)}\n\n'
    #                    f'Hey, {member.mention} Thanks for joining **{member.guild.name}**\n\n'
    #                    f'Make sure to check <#{int(cfg.RULES)}>\n'
    #                    f'Order FX over at <#{int(cfg.ORDER)}>\n\n'
    #                    f'Thank you for joining.\n'
    #                    f'Hope you like your stay here.')
    #
    #     embed = discord.Embed(
    #         title='__Graphics Code__', description=description, color=discord.Color(0xFFFFFF))
    #     embed.timestamp = discord.utils.utcnow()
    #     embed.set_footer(
    #         text=f'{member.guild.name} | {member.guild.id}', icon_url=member.guild.icon.url)
    #     # embed.set_thumbnail(url=member.guild.icon.url)
    #     embed.set_image(
    #         url='https://media.discordapp.net/attachments/992660600746422312/1026378384437161984/welcome.gif')
    #     channel = member.guild.get_channel(cfg.WELCOME)
    #     await channel.send(f"{member.mention}", embed=embed, view=view)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        embed=discord.Embed(color=cfg.CLR, title="ㅤ**WELCOME TO GRAPHICS CODE**")
        button1 = Button(label='Rules', url="https://discord.com/channels/905665593267609631/905678231896723486",
                       emoji='<:rules:1064514958278266931>')

        button2 = Button(label='Info',
                       url="https://discord.com/channels/905665593267609631/992660615833325629",
                       emoji='<:gc:1150762439789527100>')

        button3 = Button(label='Store',
                       url="https://discord.com/channels/905665593267609631/992660626272964629",
                       emoji='<:store:1064877285859147817>')

        view = View()
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        embed.description = f"""
⪦━━━━━━━━━━━━━━━━━━━━━━━⪧
**Thankyou for Joining as __{member.guild.member_count}th__ Member!**

<a:_:1034357651703865424> __Go through the rules you need to follow__
<a:_:1034357783690236025> **| Server Guidelines:** <#905678231896723486>
<a:_:1034357651703865424> __Checkout what all we offer__
<a:_:1034357783690236025> **| FX Store:** <#1064869618772090951>
<a:_:1034357651703865424> __Get your creative solutions__
<a:_:1034357783690236025> **| Order Placement:** <#992660626272964629>
<a:_:1034357651703865424> __Join us as a Designer__
<a:_:1034357783690236025> **| Apply as Designer:** <#992660663858122752>
<a:_:1034357651703865424> __Join us as a Staff Member__
<a:_:1034357783690236025> **| Apply as Staff:** <#992660662415269919>
<a:_:1034357651703865424> __Show some love & support back__
<a:_:1034357783690236025> **| Support Us:** <#992660615833325629>
⪦━━━━━━━━━━━━━━━━━━━━━━━⪧
**HAVE A GOOD STAY ♡**"""
        embed.set_image(url="https://media.discordapp.net/attachments/1150321238997205002/1150359106008395846/welcome.png?width=1025&height=202")
        embed.set_footer(text=f'{member.guild.name} | {member.guild.id}', icon_url=member.guild.icon.url)
        channel = member.guild.get_channel(cfg.WELCOME)
        await channel.send(content=member.mention,embed=embed, view=view)
        await member.send(embed=embed, view=view)




    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        description = (f'**{member.name}** just left us.\n'
                       f"We're now **{len(member.guild.members)}** members.\n")
        embed = discord.Embed(
            title='Farewell', description=description, color=cfg.CLR)
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(
            text=f'{member.guild.name} | {member.guild.id}', icon_url=member.guild.icon.url)

        channel = member.guild.get_channel(cfg.FAREWELL)
        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(WELCOME(bot))
