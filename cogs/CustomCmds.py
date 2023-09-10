import discord
from discord.ext import commands
from discord.ext import tasks
from discord.ui import View, Button
from discord import Embed
import RosterConfig as rcfg
import config as cfg
from discord import app_commands
from datetime import datetime



class CustomCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        self.auto_roster.start()

    # 3600 - 1 hr
    @tasks.loop(seconds=3600)
    async def auto_roster(self):
        guild = self.bot.get_guild(int(905665593267609631))
        FOUNDER = guild.get_role(992648475634315355)
        OWNER = guild.get_role(992648660166910073)
        BOT_DEV = guild.get_role(992651330466361414)
        DESIGNERS = guild.get_role(992651587577196686)

        foun = ", \n".join([member.name for member in FOUNDER.members])
        owne = ", \n".join([member.name for member in OWNER.members])
        botdev = ", \n".join([member.name for member in BOT_DEV.members])
        dnrs = ", \n".join([member.name for member in DESIGNERS.members])

        embed = discord.Embed(color=rcfg.CLR, timestamp=discord.utils.utcnow())
        embed.set_footer(text="Last updated on")
        embed.title = "GRAPHICS CODE 2.0 ROSTER"
        embed.add_field(name=f'<:graphicscode:985936754446073958> 𒁍〢__FOUNDERS:__ ', value=f'{foun}' or 'None',
                        inline=False)
        embed.add_field(name=f'<:graphicscode:985936754446073958> 𒁍〢__CEO:__ ', value=f'{owne}' or 'None',
                        inline=False)
        embed.add_field(name=f'<:graphicscode:985936754446073958> 𒁍〢__BOT DEVS:__ ', value=f'{botdev}' or 'None',
                        inline=False)
        embed.add_field(name=f'<:graphicscode:985936754446073958> 𒁍〢__DESIGNERS:__ ', value=f'{dnrs}' or 'None',
                        inline=False)

        embed.set_image(
            url="https://media.discordapp.net/attachments/992660602059247616/1026674654531829770/ezgif.com-gif-maker_13.gif")
        channel = guild.get_channel(rcfg.channel)
        message = await channel.fetch_message(rcfg.msgid)
        await message.edit(embed=embed)

    @auto_roster.before_loop
    async def before_looping(self):
        print('waiting for bot to get ready')
        await self.bot.wait_until_ready()
        print('looping')

    @commands.command(description='Sends roster')
    @commands.has_permissions(administrator=True, )
    async def send_roster(self, ctx):
        guild = self.bot.get_guild(int(905665593267609631))
        FOUNDER = guild.get_role(992648475634315355)
        OWNER = guild.get_role(992648660166910073)
        BOT_DEV = guild.get_role(992651330466361414)
        DESIGNERS = guild.get_role(992651587577196686)

        foun = ", \n".join([member.mention for member in FOUNDER.members])
        owne = ", \n".join([member.mention for member in OWNER.members])
        botdev = ", \n".join([member.mention for member in BOT_DEV.members])
        dnrs = ", \n".join([member.mention for member in DESIGNERS.members])

        embed = discord.Embed(color=rcfg.CLR)
        embed.title = "GRAPHICS CODE 2.0 ROSTER"
        embed.add_field(name=f'<:graphicscode:985936754446073958> 𒁍〢__FOUNDERS:__ ', value=f'{foun}' or 'None',
                        inline=False)
        embed.add_field(name=f'<:graphicscode:985936754446073958> 𒁍〢__CEO:__ ', value=f'{owne}' or 'None',
                        inline=False)
        embed.add_field(name=f'<:graphicscode:985936754446073958> 𒁍〢__BOT DEVS:__ ', value=f'{botdev}' or 'None',
                        inline=False)
        embed.add_field(name=f'<:graphicscode:985936754446073958> 𒁍〢__DESIGNERS:__ ', value=f'{dnrs}' or 'None',
                        inline=False)
        embed.set_image(
            url="https://media.discordapp.net/attachments/992660602059247616/1026674654531829770/ezgif.com-gif-maker_13.gif")
        await ctx.send(embed=embed)

        @commands.hybrid_command(aliases=['social'], description="Sends socials of Graphics Code")
        async def socials(self, ctx):
            button1 = Button(label='Youtube', url="https://www.youtube.com/channel/UCkg7ENwco4Nf0mNBJJi9qWw",
                             emoji='<:YouTube:926350797019701308>')

            button2 = Button(label='Behance',
                             url="https://behance.net/graphicscode1",
                             emoji='<Be:1024981938500554752>')

            button3 = Button(label='Instagram',
                             url="https://instagram.com/graphics_code_21",
                             emoji='<:Instagram:982250379884507186>')

            button4 = Button(label='Website',
                             url="https://graphiccodes.xyz/",
                             emoji='<website:1024982468861902868>')

            view = View()
            view.add_item(button1)
            view.add_item(button2)
            view.add_item(button3)
            view.add_item(button4)
            await ctx.send("Choose the social media that you would like to follow!", view=view)

    @commands.hybrid_command(aliases=['ab', 'bot', 'aboutbot'], description="information about the bot")
    async def botinfo(self, ctx):
        embed = discord.Embed(
            title='<a:gc_ShinyDot:949181495497621514> __Bot Information__ <a:gc_ShinyDot:949181495497621514>',
            description=f'{self.bot.description}', color=(cfg.CLR))
        embed.add_field(name='<a:black_dot1:949181553295114310> Name', value=f'```{self.bot.user.name}```',
                        inline=False)
        embed.add_field(name='<a:black_dot1:949181553295114310> Created on',
                        value=f'```{(self.bot.user.created_at.strftime(f"%d/%m/%y"))}```', inline=True)
        embed.add_field(name='<a:black_dot1:949181553295114310> Library', value=f'```discord.py v2```', inline=True)
        embed.add_field(name='<a:black_dot1:949181553295114310> Ping',
                        value=f'```{round(self.bot.latency * 1000)}ms```', inline=True)
        embed.add_field(name='<a:black_dot1:949181553295114310> Api version', value=f"```{discord.__version__}```",
                        inline=True)
        embed.add_field(name='<a:black_dot1:949181553295114310> Bot version', value=f'```v5.1```', inline=True)
        embed.add_field(name='<a:black_dot1:949181553295114310> Developers',
                        value=f'```HELLTRONIX#5209, Poison Tribbiani#0057, Lxghtning~#0388```', inline=False)
        embed.add_field(name='<a:black_dot1:949181553295114310> Servers', value=f'```{len(self.bot.guilds)}```',
                        inline=True)
        embed.add_field(name='<a:black_dot1:949181553295114310> Members', value=f'```{len(self.bot.users)}```',
                        inline=True)
        embed.add_field(name='<a:black_dot1:949181553295114310> Commands', value=f'```{len(self.bot.commands)}```',
                        inline=True)

        embed.set_footer(text=f'{self.bot.user.name} | {self.bot.user.id}', icon_url=self.bot.user.avatar.url)
        embed.timestamp = discord.utils.utcnow()
        await ctx.send(embed=embed)

    @commands.command(aliases=['dmrole'])
    @commands.has_permissions(administrator=True)
    async def dm_role(self, ctx, role: discord.Role, *, args):
        memberlist = []
        mlist = []
        for member in role.members:
            try:
                await member.send(args)
                memberlist.append(member.name)
                # mlist=", \n".join([member.mention for member in memberlist])
                mlist = ", \n".join(memberlist)
            except Exception as e:
                print(e)
        embed = discord.Embed(color=cfg.CLR, title="Direct Message sent to Members")
        embed.description = f"""
**__Role:__**
```{role}```

**__Members:__** 
```{mlist}```

**__Message:__**
```{args}```
"""
        embed.set_footer(text=f"Executed by {ctx.author}", icon_url=ctx.author.avatar)
        embed.timestamp = discord.utils.utcnow()
        channel = self.bot.get_channel(cfg.DM_LOGS_CHANNEL)
        await channel.send(embed=embed)

    @commands.hybrid_command(aliases=['ab','bot', 'aboutbot'], description="information about the bot") 
    async def botinfo(self, ctx): 
             embed= discord.Embed(title ='<a:gc_ShinyDot:949181495497621514> __Bot Information__ <a:gc_ShinyDot:949181495497621514>',            description=f'{self.bot.description}', color=(cfg.CLR)) 
             embed.add_field(name='<a:black_dot1:949181553295114310> Name', value=f'```{self.bot.user.name}```', inline=False) 
             embed.add_field(name='<a:black_dot1:949181553295114310> Created on', value=f'```{(self.bot.user.created_at.strftime(f"%d/%m/%y"))}```', inline=True) 
             embed.add_field(name='<a:black_dot1:949181553295114310> Library', value=f'```discord.py v2```', inline=True) 
             embed.add_field(name='<a:black_dot1:949181553295114310> Ping', value=f'```{round(self.bot.latency*1000)}ms```', inline=True) 
             embed.add_field(name='<a:black_dot1:949181553295114310> Api version', value=f"```{discord.__version__}```", inline=True) 
             embed.add_field(name='<a:black_dot1:949181553295114310> Bot version', value=f'```v5.1```', inline=True) 
             embed.add_field(name='<a:black_dot1:949181553295114310> Developers', value=f'```HELLTRONIX#5209, Poison Tribbiani#0057, Lxghtning~#0388```', inline=False) 
             embed.add_field(name='<a:black_dot1:949181553295114310> Servers', value=f'```{len(self.bot.guilds)}```', inline=True) 
             embed.add_field(name='<a:black_dot1:949181553295114310> Members', value=f'```{len(self.bot.users)}```', inline=True) 
             embed.add_field(name='<a:black_dot1:949181553295114310> Commands', value=f'```{len(self.bot.commands)}```', inline=True) 
  
             embed.set_footer(text = f'{self.bot.user.name} | {self.bot.user.id}', icon_url=self.bot.user.avatar.url) 
             embed.timestamp = discord.utils.utcnow() 
             await ctx.send(embed = embed)    

    @commands.hybrid_command(aliases=['social'], description="Sends socials of Graphics Code")
    async def socials(self, ctx):
        button1 = Button(label='Youtube', url="https://www.youtube.com/channel/UCkg7ENwco4Nf0mNBJJi9qWw",
                         emoji='<:YouTube:926350797019701308>')

        button2 = Button(label='Behance',
                         url="https://behance.net/graphicscode1",
                         emoji='<Be:1024981938500554752>')

        button3 = Button(label='Instagram',
                         url="https://instagram.com/graphics_code_21",
                         emoji='<:Instagram:982250379884507186>')

        button4 = Button(label='Twitter',
                         url="https://twitter.com/GraphicsCode21",
                         emoji='<:Twitter:962739971104579594>')
        
        button5 = Button(label='Website',
                         url="https://graphiccodes.xyz/",
                         emoji='<website:1024982468861902868>')


        view = View()
        view.add_item(button1)
        view.add_item(button2)
        view.add_item(button3)
        view.add_item(button4)
        view.add_item(button5)
        await ctx.send("Our Socials", view=view)
        
    @commands.hybrid_command(aliases=['message'], description="Direct message a user")
    @commands.has_permissions(administrator=True)
    async def dm(self, ctx, member: discord.Member, *, message):
        try:
            await member.send(message)
            await ctx.send(f"```{message}``` sent to {member.name}#{member.discriminator}")
            logembed = discord.Embed()
            logembed.title = f'Direct Message send to: __`{member.name}{member.discriminator}`__'
            logembed.description = f'''
            **__Message:__** 
            ```{message}``` '''
            logembed.color = cfg.CLR
            logembed.set_footer(text=f"Executed by {ctx.author}", icon_url=ctx.author.avatar)
            dmchannel = discord.utils.get(ctx.guild.channels, id=cfg.cfg.DM_LOGS_CHANNEL)
            await dmchannel.send(embed=logembed)
        except:
            return await ctx.send('<a:mave_cross:932299292075515946> Logging has failed!')

    @commands.command(aliases=['dmr'])
    @commands.has_permissions(administrator=True)
    async def dm_role(self, ctx, role: discord.Role, *, args):
        memberlist = []
        mlist = []
        for member in role.members:
            try:
                await member.send(args)
                memberlist.append(member.name)
                # mlist=", \n".join([member.mention for member in memberlist])
                mlist = ", \n".join(memberlist)
            except Exception as e:
                print(e)
        embed = discord.Embed(color=cfg.CLR, title="Direct Message sent to Members")
        embed.description = f"""
**__Role:__**
```{role}```

**__Members:__** 
```{mlist}```

**__Message:__**
```{args}```
"""
        embed.set_footer(text=f"Executed by {ctx.author}", icon_url=ctx.author.avatar)
        embed.timestamp = discord.utils.utcnow()
        channel = self.bot.get_channel(cfg.DM_LOGS_CHANNEL)
        await channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def rules_embed(self, ctx):
        embed1=discord.Embed(color=cfg.CLR)
        embed1.description = desc1
        embed2=discord.Embed(color=cfg.CLR)
        embed2.description = desc2
        embed3=discord.Embed(color=cfg.CLR)
        embed3.description = desc3
        embed4=discord.Embed(color=cfg.CLR)
        embed4.description = desc4
        embed5 = discord.Embed(color=cfg.CLR)
        embed5.set_image(url="https://cdn.discordapp.com/attachments/1150321238997205002/1150333919112216606/rules.png")
        embeds = [embed1, embed2, embed3, embed4]
        await ctx.send(embeds=embeds)
        await ctx.message.delete()


async def setup(bot):
    await bot.add_cog(CustomCmds(bot))

desc1 = """
ㅤㅤ     **RULES OF GRAPHICS CODE 2.0**
⪦━━━━━━━━━━━━━━━━━━━━━━━⪧

               <:_:1034833534164140104>**Moderation System**<:_:1034833534164140104>

<:_:1034833385543172136> **__BASIC INFORMATION__**
> Moderation Team will impose strikes according to the below mentioned __Strike Policy__ taking into account your history & graveness of your violation of the rules. All actions are taken after thorough investigation & collection of evidence.
<:_:1034833385543172136> **__STRIKE POLICY__**
> First Strike: Warning
> Second Strike: Mute (24 Hours)
> Third Strike: Ban (3 Days)
> Fourth Strike: Permanent Ban
<:_:1034833385543172136> **__NOTE__**
> Number of strikes given depends on the situation. We can give four strikes together also so be aware & follow all the rules.

⪦━━━━━━━━━━━━━━━━━━━━━━━⪧"""

desc2 = """
ㅤㅤ     **RULES OF GRAPHICS CODE**
⪦━━━━━━━━━━━━━━━━━━━━━━━⪧

               <:_:1034833534164140104>**General Instructions**<:_:1034833534164140104>

<:_:1034833385543172136> **__NO DEFAMATORY LANGUAGE__**
> Using defamatory words or cussing anyone in any situation with the intention to harm anyone mentally is strictly prohibited. Using such language casually & to improvise humour is allowed upto a certain mark.
<:_:1034833385543172136> **__NO NSFW CONTENT__**
> Sharing sexually implicit content or non-consensual intimate images/links is not allowed.
<:_:1034833385543172136> **__NO SPAMMING/EARRAPING__**
> Spamming of every kind whether it is text-based or voice chat based including earraping, playing discomposed music & purposeful intrusion in discussions of others during day-to-day activity or events is strictly prohibited.
<:_:1034833385543172136> **__TREAT EVERYONE EQUALLY __**
> Treat everyone equally with respect & appreciate sentiments of everyone irrespective of caste, creed, gender, religion & other beliefs.
<:_:1034833385543172136> **__NO UNETHICAL ADVERTISING__**
> Promoting unlawful/violent content or product is not allowed.
> DM Promotion through individuals or bots targeting people of our server is not allowed.
<:_:1034833385543172136> **__NO ILLEGAL ACTIVITIES__**
> Practicing disobedient behaviour or sharing private information about others without their consent & posting malicious links to fraud/scam websites, supporting hacking or DDOS attacks is strictly prohibited.
> Trading illegal things of any sort for personal interest is also prohibited.

⪦━━━━━━━━━━━━━━━━━━━━━━━⪧"""

desc3 = """
ㅤㅤ     **RULES OF GRAPHICS CODE**
⪦━━━━━━━━━━━━━━━━━━━━━━━⪧

               <:_:1034833534164140104>**Ticket Instructions**<:_:1034833534164140104>

<:_:1034833385543172136> **__ORDER DISCUSSIONS__**
> No discussions related to the order to be done in DMs or in any other channel. All order related talks need to be done in the ticket itself including placement of orders, asking for updates, payment process & claiming the design as everything needs to be logged for further use.
<:_:1034833385543172136> **__CODE OF CONDUCT__**
> Fill out the forms correctly while placing the orders.
> Be a little elaborate to everything you mention for giving the designer a better idea to take care of your needs.
> Insulting or disrespecting any staff/designer for your personal interest or with the intention to defame anyone is not allowed. 
<:_:1034833385543172136> **__TICKET CREATION__**
> Create tickets only if you meet the order requirements & are willing to buy something. Don't open tickets with the intention of wasting time & efforts of others.
<:_:1034833385543172136> **__DESIGN PRICES __**
> Negotiation in prices is not allowed. Minimum price of every design is fixed & everyone need to follow up that unless any event/offer is in progress. 

⪦━━━━━━━━━━━━━━━━━━━━━━━⪧"""

desc4 = """
ㅤㅤ     **RULES OF GRAPHICS CODE 2.0**
⪦━━━━━━━━━━━━━━━━━━━━━━━⪧

               <:_:1034833534164140104>**Things to be Noted**<:_:1034833534164140104>

<:_:1034833385543172136> **__ALTS/MULTIPLE ACCOUNTS__**
> Using multiple accounts for trolling/disturbing others, evading bans, mutes & other restrictions or to increase chances of winning any sort of giveaway/event is strictly prohibited.
<:_:1034833385543172136> **__MESSAGING STAFFS__**
> Messaging staff or management on personal window for any sort of query related to this server is prohibited. Instead use ModMail to connect with higher authorities of the server.
<:_:1034833385543172136> **__LOOPHOLES__**
> In case you find something unusual happening or any sort of error in any part of the server including the Official Bot, make sure to report it to the moderators or higher authorities promptly. Exploiting loopholes or encouraging such kind of action is strictly prohibited.

⪦━━━━━━━━━━━━━━━━━━━━━━━⪧"""

