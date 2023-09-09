import time
import discord
from discord.ext import commands
import config as cfg
import json
import asyncio


class BUTTON1(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label='Claim', style=discord.ButtonStyle.green, custom_id='Claim:green')
    async def Claim(self, button=discord.ui.Button, interaction=discord.Interaction):
        artists = interaction.guild.get_role(int(cfg.ARTISTS))
        if artists in interaction.user.roles:
            pass
        else:
            await interaction.response.send_message(
                f'You are not a valid artist in this server.\nOnly artists are allowed to claim an order.',
                ephemeral=True)
            return

        with open('cogs/orders.json', 'r') as f:
            data = json.load(f)

        client = interaction.guild.get_member(int(data["CHANNELS"][str(interaction.channel.id)]))

        embed = discord.Embed(title='ORDER CLAIMED',
                              description=f'{client.mention} your order was accepted by our artist - {interaction.user.mention}.',
                              color=discord.Color(0x2C2F33))
        embed.timestamp = discord.utils.utcnow()
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)

        # async for message in interaction.channel.history():
        #        if message.author.id == int(cfg.BOT):
        #               await message.delete()
        view = BUTTON2(self.bot)
        await interaction.message.delete()
        msg = await interaction.channel.send(embed=embed, view=view)
        await msg.pin()

        data["CURRENT"][str(client.id)] = interaction.user.id

        with open('cogs/orders.json', 'w') as f:
            json.dump(data, f, indent=4)

        embed.set_thumbnail(url=interaction.guild.icon.url)
        embed.color = discord.Color(0x00FF00)
        embed.add_field(name='Link', value=f'[You can view the message here]({msg.jump_url})')
        try:
            await client.send(embed=embed)
        except:
            await interaction.channel.send(content=f"{client.mention}", embed=embed)
        await interaction.channel.edit(name=f'claimed-{client.name}')

        overwrites = {
            interaction.user: discord.PermissionOverwrite(
                send_messages=True,
                view_channel=True,
                manage_messages=False,
                manage_channels=False,
                manage_permissions=False
            ),

            artists: discord.PermissionOverwrite(
                view_channel=False
            ),

            interaction.guild.default_role: discord.PermissionOverwrite(
                view_channel=False
            ),

            client: discord.PermissionOverwrite(
                send_messages=True,
                view_channel=True,
                manage_messages=False,
                manage_channels=False,
                manage_permissions=False
            )
        }

        await interaction.channel.edit(overwrites=overwrites)
        return

    @discord.ui.button(label='Reject', style=discord.ButtonStyle.blurple, custom_id='reject1:blurple')
    async def reject(self, button=discord.ui.Button, interaction=discord.Interaction):
        artists = interaction.guild.get_role(int(cfg.ARTISTS))
        if artists in interaction.user.roles:
            pass
        else:
            await interaction.response.send_message(f'Oops you dont have the permissions to reject an order.',
                                                    ephemeral=True)

        embed = discord.Embed(title='Order Rejected',
                              description=f'Your Order in **{interaction.guild.name}** was cancelled by **{interaction.user.name}**',
                              color=discord.Color(0xFF1100))
        embed.timestamp = discord.utils.utcnow()
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_footer(text=f'{interaction.guild.name} | {interaction.guild.id}')

        with open('cogs/orders.json', 'r') as f:
            data = json.load(f)

        client = interaction.guild.get_member(int(data["CHANNELS"][str(interaction.channel.id)]))
        await client.send(embed=embed)
        await interaction.channel.delete()

        data['CHANNELS'].pop(str(interaction.channel.id))

        with open('cogs/orders.json', 'w') as f:
            json.dump(data, f, indent=4)

        return

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.danger, custom_id='cancel1:red')
    async def cancel(self, button=discord.ui.Button, interaction=discord.Interaction):
        with open('cogs/orders.json', 'r') as f:
            data = json.load(f)
        artists = interaction.guild.get_role(int(cfg.ARTISTS))

        if interaction.user.id == int(data['CHANNELS'][str(interaction.channel.id)]):
            pass
        else:
            if artists in interaction.user.roles:
                pass
            else:
                await interaction.response.send_message(
                    f'You did not open this ticket and neither are an artist.\nPlease ask the owner of the ticket or any moderator to close the ticket instead.',
                    ephemeral=True)
                return
        await interaction.response.send_message(f'This ticket was cancelled.')
        time.sleep(10)
        await interaction.channel.delete()

        data['CHANNELS'].pop(str(interaction.channel.id))
        with open('cogs/orders.json', 'w') as f:
            json.dump(data, f, indent=4)


class BUTTON2(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label='Complete', style=discord.ButtonStyle.green, custom_id='complete:green')
    async def complete(self, button=discord.ui.Button, interaction=discord.Interaction):
        with open('cogs/orders.json', 'r') as f:
            data = json.load(f)

        client = interaction.guild.get_member(int(data["CHANNELS"][str(interaction.channel.id)]))
        artist = interaction.guild.get_member(int(data['CURRENT'][str(client.id)]))
        artists = interaction.guild.get_role(int(cfg.ARTISTS))
        if interaction.user.id == artist.id:
            pass
        else:
            await interaction.response.send_message(
                f'{artist.mention} artist claimed this order and is currently working on it. This order cannot be claimed by you.',
                ephemeral=True)
            return

        await receipt(self.bot, interaction, client, artist)

    @discord.ui.button(label='Unclaim', style=discord.ButtonStyle.blurple, custom_id='unclaim:blurple')
    async def unclaim(self, button=discord.ui.Button, interaction=discord.Interaction):
        await interaction.message.delete()

        with open('cogs/orders.json', 'r') as f:
            data = json.load(f)

        data['CURRENT'].pop(str(data['CHANNELS'][str(interaction.channel.id)]))

        with open('cogs/orders.json', 'w') as f:
            json.dump(data, f, indent=4)

        client = discord.utils.get(interaction.guild.members, id=(int(data['CHANNELS'][str(interaction.channel.id)])))

        artists = interaction.guild.get_role(int(cfg.ARTISTS))

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                send_messages=False,
                view_channel=False,
                manage_messages=False,
                manage_channels=False,
                manage_permissions=False
            ),
            artists: discord.PermissionOverwrite(
                send_messages=True,
                view_channel=True,
                read_messages=True,
                manage_messages=False,
                manage_channels=False,
                manage_permissions=False
            ),
            client: discord.PermissionOverwrite(
                send_messages=True,
                view_channel=True,
                manage_messages=False,
                manage_channels=False,
                manage_permissions=False
            )
        }
        await interaction.channel.edit(name=f"unclaimed-{client.name}", overwrites=overwrites)
        embed = discord.Embed(title=f'Place Your Order',
                              description=f'Place an order here.\nType `%procedure` to know the Procedure.\n`%price` to know basic price chart.\n`%form` to fill the form for our artists to understand your idea.',
                              color=discord.Color(0x2C2F33))
        embed.set_footer(text=f'{interaction.guild.name} | {interaction.guild.id}', icon_url=interaction.guild.icon.url)
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.timestamp = discord.utils.utcnow()
        view = BUTTON1(self.bot)
        msg = await interaction.channel.send(content=f'<@&{cfg.ARTISTS}>', embed=embed, view=view)
        await msg.pin()

    @discord.ui.button(label='Reject', style=discord.ButtonStyle.blurple, custom_id='reject2:blurple')
    async def reject(self, button=discord.ui.Button, interaction=discord.Interaction):
        with open('cogs/orders.json', 'r') as f:
            data = json.load(f)

        client = interaction.guild.get_member(int(data['CHANNELS'][str(interaction.channel.id)]))
        artist = interaction.guild.get_member(int(data['CURRENT'][str(client.id)]))

        if interaction.user.id == artist.id:
            pass
        else:
            await interaction.response.send_message(
                f'You did not claim this Order, hence it cannot be cancelled by you.', ephemeral=True)
            return

        data['CURRENT'].pop(str(client.id))
        data['CHANNELS'].pop(str(interaction.channel.id))

        with open('cogs/orders.json', 'w') as f:
            json.dump(data, f, indent=4)

        embed = discord.Embed(title='Order Rejected',
                              description=f'Your Order in **{interaction.guild.name}** was cancelled by **{interaction.user.name}**',
                              color=discord.Color(0xFF1100))
        embed.timestamp = discord.utils.utcnow()
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_footer(text=f'{interaction.guild.name} | {interaction.guild.id}')

        await client.send(embed=embed)
        return

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.danger, custom_id='cancel2:red')
    async def cancel(self, button=discord.ui.Button, interaction=discord.Interaction):
        with open('cogs/orders.json', 'r') as f:
            data = json.load(f)

        client = interaction.guild.get_member(int(data['CHANNELS'][str(interaction.channel.id)]))
        artist = interaction.guild.get_member(int(data['CURRENT'][str(client.id)]))

        if interaction.user.id == client.id:
            pass
        else:
            await interaction.response.send_message(
                f'You are not the client of this particular Order. You cannot cancel it.', ephemeral=True)
            return

        data['CURRENT'].pop(str(client.id))
        data['CHANNELS'].pop(str(interaction.channel.id))

        with open('cogs/orders.json', 'w') as f:
            json.dump(data, f, indent=4)

        embed = discord.Embed(title='Order Cancelled',
                              description=f'Order Placed by {client.mention} in **{interaction.guild.name} was cancelled by them.**',
                              color=discord.Color(0xFF1100))
        embed.timestamp = discord.utils.utcnow()
        embed.set_thumbnail(url=interaction.guild.icon)
        embed.set_footer(text=f'{interaction.guild.name} | {interaction.guild.id}')

        await artist.send(embed=embed)
        return


class Confirmation(discord.ui.View):
    def __init__(self, artist, client, bot, embed, number):
        self.embed = embed
        self.artist = artist
        self.client = client
        self.number = number
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green, custom_id='Confirm:green')
    async def conf(self, button=discord.ui.Button, interaction=discord.Interaction):
        if interaction.user.id == self.artist.id:
            pass
        else:
            await interaction.response.send_message(
                f'You are not the artist. Please ask {self.artist.mention} to complete the proceduer.', ephemeral=True)
        await interaction.message.delete()
        interaction_channel = interaction.channel
        self.embed.set_author(name=f'#{self.number}')
        channel = self.bot.get_channel(int(cfg.COMPLETED))
        await channel.send(embed=self.embed)
        await interaction.channel.send(embed=self.embed)

        overwrites = {
            self.client: discord.PermissionOverwrite(
                send_messages=False
            )
        }
        await interaction.channel.edit(overwrites=overwrites)
        await interaction.channel.edit(name=f'completed-{self.client.name}')

        with open('cogs/orders.json', 'r') as f:
            data = json.load(f)

        data['CURRENT'].pop(str(self.client.id))
        data['CHANNELS'].pop(str(interaction_channel.id))

        data['TOTALORDERS'] = str(int(data['TOTALORDERS']) + 1)
        try:
            data['COMPLETED_ORDERS'][str(self.artist.id)] = int(data['COMPLETED_ORDERS'][str(self.artist.id)]) + 1
        except:
            data['COMPLETED_ORDERS'][str(self.artist.id)] = 1

        with open('cogs/orders.json', 'w') as f:
            json.dump(data, f, indent=4)
        clients = discord.utils.get(interaction.guild.roles, id=int(cfg.CLIENT))
        await self.client.add_roles(clients)

        def rate(rating):
            rating.author.id == self.client.id and rating.isdigit() and rating.channel.id == interaction.channel.id

        channel = interaction.channel
        # await channel.send(f"How would you rate {self.artist.mention}'s work on a scale of 1-10?")
        # rating = await self.bot.wait_for('message', check = rate())

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.danger, custom_id='cancel3:red')
    async def can(self, button=discord.ui.Button, interaction=discord.Interaction):
        if interaction.user.id == self.artist.id:
            pass
        else:
            await interaction.response.send_message(
                f'You are not the artist. Please ask {self.artist.mention} to complete the proceduer.', ephemeral=True)
        await interaction.message.delete()
        await interaction.channel.send(f'Aborted', delete_after=10)
        with open('cogs/orders.json', 'r') as f:
            data = json.load(f)

        data['ORDERS'].pop(str(self.number))

        with open('cogs/orders.json', 'w') as f:
            json.dump(data, f, indent=4)

        embed = discord.Embed(title='ORDER CLAIMED',
                              description=f'{self.client.mention} your order was accepted by our artist - {interaction.user.mention}.',
                              color=discord.Color(0x2C2F33))
        embed.timestamp = discord.utils.utcnow()
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        embed.set_footer(text=f'Regards, Team {interaction.guild.name}')

        # async for message in interaction.channel.history():
        #        if message.author.id == int(cfg.BOT):
        #               await message.delete()
        await interaction.message.delete()
        view = BUTTON2(self.bot)
        msg = await interaction.channel.send(embed=embed, view=view)
        await msg.pin()

        # data["CURRENT"][str(client.id)] = interaction.user.id

        # with open('cogs/orders.json', 'w') as f:
        #        json.dump(data, f, indent = 4)

        # embed.set_thumbnail(url=interaction.guild.icon)
        # embed.color = discord.Color(0x00FF00)
        # embed.add_field(name = 'Link',value = f'[You can view the message here]({msg.jump_url})')

        # await client.send(embed=embed)
        # await interaction.channel.edit(name=f'claimed-{client.name}')
        # return


async def receipt(bot, interaction, client, artist):
    channel = interaction.channel

    def check(message):
        return message.author.id == artist.id and message.channel == channel

    await channel.send(f'{artist.mention} Enter Payment Method. (Paytm/Gpay/Invites/etc)')

    payment = await bot.wait_for('message', check=check, timeout=None)
    # print(payment.content)
    await channel.send(f'Enter work type. (PFP/Banner/Thumbnail/etc)')

    work = await bot.wait_for('message', check=check, timeout=None)
    # print(work.content)
    await channel.send(f'Enter Style. (Vector art/etc.)')

    style = await bot.wait_for('message', check=check, timeout=None)
    # print(style.content)
    await channel.send(f'Enter Price for the design. (Invites or Money)')

    price = await bot.wait_for('message', check=check, timeout=None)
    # print(price.content)
    await channel.send(f'Enter **LINK** for the design.')

    link = await bot.wait_for('message', check=check, timeout=None)
    # print(link.content)
    embed = discord.Embed(title='Order Receipt',
                          description=f'This is a receipt for {work.content} ordered by {client.mention} which was completed by {artist.mention}.',
                          color=discord.Color(0x00FF00))
    embed.set_footer(text=f'{interaction.user.name} | {interaction.user.id}', icon_url=interaction.user.avatar.url)
    embed.timestamp = discord.utils.utcnow()
    value = (f'**Artist** - {artist.mention}\n'
             f'**Client** - {client.mention}\n'
             f'**Payment** - {(payment.content).upper()}\n'
             f'**Work** - {work.content.upper()}\n'
             f'**Style** - {style.content.upper()}\n'
             f'**Price** - {price.content}\n')
    # f'**[Link]({link.content})**'
    embed.add_field(name='Order Details', value=value)
    try:
        embed.set_image(url=link.content)
    except:
        await link.channel.send(f'Invalid link. Try again')
        return

    with open('cogs/orders.json', 'r') as f:
        data = json.load(f)

    order_details = {
        "CLIENT": client.id,
        "ARTIST": artist.id,
        "PAYMENT": str(payment.content),
        "WORK": str(work.content),
        "STYLE": str(style.content),
        "PRICE": str(price.content),
        "LINK": str(link.content)
    }

    ordernum = 0
    bool = False
    while bool == False:
        try:
            data['ORDERS'][str(ordernum)]
            ordernum += 1

        except:
            data['ORDERS'][ordernum] = order_details
            bool = True

    view = Confirmation(artist, client, bot, embed, ordernum)
    # async for message in interaction.channel.history():
    #               if message.author.id == int(cfg.BOT):
    #                      await message.delete()
    await channel.send(embed=embed, view=view)

    #############################################

    #############################################
    with open('cogs/orders.json', 'w') as f:
        json.dump(data, f, indent=4)