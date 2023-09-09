import asyncio
import time

import discord
from discord.ext import commands

import config as cfg


class ModMail(commands.Cog):
    """ModMail COG that handles with the ModMail System  and its functioning"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild == None:
            return
        if message.author == self.bot.user:
            return

        guild = self.bot.get_guild(int(cfg.GUILD))

        embed = discord.Embed(title="ModMail.", description=f"You are sending this message to **{guild.name}**.\n"
                                                            f'React with ✅ to Confirm.\n'
                                                            f'React with ❎ to Cancel.', color=discord.Color(cfg.CLR))
        if not guild.icon is None:
            embed.set_author(name=guild.name, icon_url=guild.icon.url)
            embed.set_thumbnail(url=guild.icon)
            embed.set_footer(text=f'{guild.name} | {guild.id}', icon_url=guild.icon.url)
        else:
            embed.set_author(name=guild.name)
            embed.set_footer(text=f'{guild.name} | {guild.id}')

        msg = None
        try:
            msg = await message.channel.send(embed=embed)
        except:
            return
        reactions = ['✅', '❎']
        for reaction in reactions:
            await msg.add_reaction(reaction)

        try:
            def check(reaction, user):
                return str(reaction.emoji) in reactions and user != self.bot.user

            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=600)
            if str(reaction.emoji) == '❎':
                await msg.delete()
                await message.channel.send('Aborted')
                return

            if str(reaction.emoji) == '✅':
                channel = discord.utils.get(guild.text_channels, name=f'{str(message.author)}',
                                            topic=f'{str(message.author.id)}')
                if channel == None:
                    categ = discord.utils.get(guild.categories, id=999317375868481706)
                    channel = await categ.create_text_channel(name=str(message.author),
                                                              topic=f'{str(message.author.id)}')
                    for role in guild.roles:
                        if role.permissions.manage_guild == True:
                            overwrites = {
                                guild.default_role: discord.PermissionOverwrite(
                                    view_channel=False,
                                ),
                                role: discord.PermissionOverwrite(
                                    view_channel=True,
                                    read_messages=True,
                                    send_messages=True,
                                )
                            }
                            await channel.edit(overwrites=overwrites)
                poison = self.bot.get_user(int(cfg.OWNER))
                try:
                    poison = self.bot.get_user(int(cfg.OWNER))
                    embed = discord.Embed(title='ModMail', color=discord.Color(cfg.CLR))
                    embed.timestamp = discord.utils.utcnow()
                    embed.description = (f'{message.content}')
                    embed.set_author(name=message.author.name, icon_url=message.author.avatar.url)
                    if not guild.icon is None:
                        embed.set_thumbnail(url=guild.icon)
                    embed.set_footer(text=f'Bot Developed by {poison.name} | {poison.id}',
                                     icon_url=poison.display_avatar.url)

                    await channel.send(embed=embed)

                    embed = discord.Embed(title='Message Sent', color=discord.Color(cfg.CLR))
                    embed.description = (
                        f'Your message was successfully sent to **{guild.name}**. Please wait for further response.')
                    if not guild.icon is None:
                        embed.set_author(name=f'{guild.name} | {guild.id}', icon_url=guild.icon.url)
                    else:
                        embed.set_author(name=f'{guild.name} | {guild.id}')
                    embed.set_footer(text=f'Bot developed by {poison.name} | {poison.id}',
                                     icon_url=poison.display_avatar.url)
                    embed.timestamp = discord.utils.utcnow()
                    try:
                        await message.channel.send(embed=embed)
                        await msg.delete()
                        return
                    except:
                        return

                except:
                    embed = discord.Embed(title='Error!!',
                                          description=f'Sending Your message Failed. Please Contant the moderators and inform <@516439107732373514> about the flaw.',
                                          color=cfg.CLR)
                    embed.timestamp = discord.utils.utcnow()
                    try:
                        await message.channel.send(embed=embed)
                        return
                    except:
                        return

        except asyncio.TimeoutError:
            await msg.delete()
            await message.channel.send('You did not choose any option')
            return

    @commands.command()
    async def reply(self, ctx, reason):
        guild = self.bot.get_guild(int(cfg.GUILD))
        if len(reason) > 1000:
            await ctx.send('Message is too long!\nTry again with a shorter message.')
            return

        embed = discord.Embed(title=f'Mod Mail', color=discord.Color(0x000000))
        embed.description = (f'{reason}')
        embed.timestamp = discord.utils.utcnow()
        if not guild.icon is None:
            embed.set_footer(text=f'{guild.name} | {guild.id}', icon_url=guild.icon.url)
            embed.set_thumbnail(url=guild.icon.url)
        else:
            embed.set_footer(text=f'{guild.name} | {guild.id}')
        embed.set_author(name=f'{ctx.author.name} | {ctx.author.id}', icon_url=ctx.author.display_avatar.url)

        user = self.bot.get_user(int(ctx.channel.name))

        if user == None:
            await ctx.reply('The user is not present in the Server, this Channel will now be deleted.')
            time.sleep(60)
            await ctx.channel.delete()

        try:
            await user.send(embed=embed)
            embed = discord.Embed(title='Successful.',
                                  description=f'Your message was successfully sent to <@{user.id}>.',
                                  color=discord.Color(0x00FF00))
            embed.timestamp = discord.utils.utcnow()
            await ctx.send(embed=embed)
            await ctx.message.delete()
            return

        except:
            embed = discord.Embed(
                description='Your message could not be delivered. This was because the User has their DMs Closed.',
                color=discord.Color(0xFF1100))
            embed.timestamp = discord.utils.utcnow()

            await ctx.send(embed=embed)
            await ctx.message.delete()
            return

    @reply.error
    async def noarg(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('No message given.')
            return

    @commands.command()
    async def close(self, ctx, reason=None):
        guild = self.bot.get_guild(int(cfg.GUILD))
        if reason == None:
            reason = 'No reason was given.'

        if len(reason) > 1000:
            await ctx.send('Message is too long!\nTry again with a shorter message.')
            return

        embed = discord.Embed(title=f'Ticket Closed', color=discord.Color(0x000000))
        embed.description = (f'{reason}')
        embed.timestamp = discord.utils.utcnow()
        if not guild.icon is None:
            embed.set_footer(text=f'{guild.name} | {guild.id}', icon_url=guild.icon.url)
            embed.set_thumbnail(url=guild.icon.url)
        else:
            embed.set_footer(text=f'{guild.name} | {guild.id}')
        embed.set_author(name=f'{ctx.author.name} | {ctx.author.id}', icon_url=ctx.author.display_avatar.url)

        user = self.bot.get_user(int(ctx.channel.name))

        if user == None:
            await ctx.reply('The user is not present in the Server, this Channel will now be deleted.')
            time.sleep(60)
            await ctx.channel.delete()

        try:
            await user.send(embed=embed)
            embed = discord.Embed(title='Successful.', description=f'Ticket was successfully closed for <@{user.id}>.',
                                  color=discord.Color(0x00FF00))
            embed.timestamp = discord.utils.utcnow()
            await ctx.send(embed=embed)
            await ctx.message.delete()
            time.sleep(15)
            await ctx.channel.delete()

        except:
            embed = discord.Embed(
                description='Your message could not be delivered. This was because the User has their DMs Closed.',
                color=discord.Color(0xFF1100))
            embed.timestamp = discord.utils.utcnow()

            await ctx.send(embed=embed)
            await ctx.message.delete()
            time.sleep(15)
            await ctx.channel.delete()
            return


async def setup(bot):
    await bot.add_cog(ModMail(bot))
