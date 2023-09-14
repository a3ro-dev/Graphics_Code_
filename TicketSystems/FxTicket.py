import asyncio
import datetime
import aiosqlite
import discord
from discord.ext import commands
import config as cfg
from db import db

# Receipt Format

# Placed On : [DD / MM / YY]
# Completed On : [DD / MM / YY]
# Order Type : [GFx. VFx.]
# Design Category : [Category The Designs Belongs To]
# Order Style : [The Order Style]
# Payment Method : [UPI, Paytm, Gpay, Phonpe, Cashapp, Paypal, GooglePlayCode, Discord Nitro]
# Order Amount : [The Amount Paid By The Client]


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


class Receipt_Modal(discord.ui.Modal, title="Billing up.."):
    order_type = discord.ui.TextInput(
        label="Type Of Order",
        placeholder="[ GFX / VFX ]",
        required=True,
        max_length=3
    )

    categ = discord.ui.TextInput(
        label="Design Category",
        placeholder="Enter the category the design(s) belongs to",
        required=True,
        max_length=20
    )

    style = discord.ui.TextInput(
        label="Order Style",
        placeholder="Enter the Order Style",
        required=True,
        max_length=50
    )

    payment = discord.ui.TextInput(
        label="Payment Method",
        placeholder="[UPI / Paytm / Gpay / Phonpe / Cashapp / Paypal / GooglePlayCode / Discord Nitro]",
        required=True,
        max_length=15
    )

    image = discord.ui.TextInput(
        label="Image Link",
        placeholder="Enter the image url",
        required=False,
        max_length=250
    )

    async def on_submit(self, interaction):

        art = db.field("SELECT ARTIST FROM orders WHERE CHANNEL = ?", interaction.channel.id)
        client = db.field('SELECT CLIENT FROM orders WHERE CHANNEL = ?', interaction.channel.id)

        placement_date = db.field("SELECT PLACEMENT FROM orders WHERE CHANNEL = ?", interaction.channel.id)

        embed = discord.Embed(title="Order Receipt",
                              description=f"This is the receipt of the order placed by <@{client}>\n\n**ORDER DETAILS**\n**ARTIST**:- <@{art}>\n**CLIENT** :- <@{client}>\nDate of Placement :- {placement_date if placement_date is not None else 'Not found'}\nDate of Completion:- {datetime.datetime.now().strftime('%d / %m / %Y')}\nOrder :- {self.order_type.value}\nCategory Of Design:- {self.categ.value}\nStyle of Order:- {self.style.value}\nMethod Of Payment:- {self.payment.value}\n",
                              color=cfg.CLR)
        try:
            embed.set_image(url=self.image.value)
        except discord.errors.HTTPException:
            embed.set_image(url=None)
        try:
            await modal_helper(self.order_type.value, art)
        except ValueError:
            return await interaction.response.send_message(
                f"{interaction.user.mention} The argument you gave for order type was invalid")

        embed.set_footer(text=interaction.guild.name, icon_url=interaction.guild.icon.url)
        channel = discord.utils.get(interaction.guild.text_channels, id=1068049403098693682)
        await channel.send(embed=embed)
        await interaction.response.send_message(
            f"The receipt was sent to {channel} and the points was updated accordingly.")


class Receipt_Button(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Generate Receipt", style=discord.ButtonStyle.red, custom_id='receipt_custom_id')
    async def receipt_button_function(self, interaction, button):
        await interaction.response.send_modal(Receipt_Modal())
        for child in self.children:
            child.disabled = True
        self.style = discord.ButtonStyle.green


class Confirm(discord.ui.View):
    def __init__(self):
        self.value = None
        super().__init__(timeout=None)

    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green, custom_id='Yes')
    async def affirm(self, button=discord.ui.Button, interaction=discord.Interaction):
        self.value = True
        self.stop()

    @discord.ui.button(label='No', style=discord.ButtonStyle.red, custom_id='Red:No')
    async def effirm(self, button=discord.ui.Button, interaction=discord.Interaction):
        self.value = False
        self.stop()


class Buttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji='<:gfx:1064863522011488266>', style=discord.ButtonStyle.gray, custom_id='Gray:GFX')
    async def GFX_button(self, interaction=discord.Interaction, button=discord.ui.Button):
        artists = interaction.guild.get_role(cfg.ARTISTS)
        ticket_supp = interaction.guild.get_role(cfg.SUPPORT)
        client_role = interaction.guild.get_role(cfg.CLIENT)
        community = interaction.guild.get_role(cfg.COMMUNITY)

        client = interaction.user
        categ = discord.utils.get(interaction.guild.categories, id=cfg.ORDER_TICK)
        channel = await categ.create_text_channel(name=f'GFX-{client.name}')
        await channel.set_permissions(interaction.guild.default_role, view_channel=False)
        await channel.set_permissions(interaction.user, view_channel=True, send_messages=True)
        await channel.set_permissions(ticket_supp, view_channel=True, send_messages=True,
                                      send_messages_in_threads=False)
        await channel.set_permissions(artists, view_channel=True, send_messages=True, send_messages_in_threads=False)
        # await channel.set_permissions(client_role, view_channel=False)
        await channel.set_permissions(community, view_channel=False)

        embed = discord.Embed(title='GFX Ticket',
                              description=f'Ticket Opened by {client.mention}\nCustomer Support will be with you shortly.\nCheck pricing and other information by using `%procedure`, `%price`, `%form`.',
                              color=discord.Color(0x2F3136))
        embed.timestamp = discord.utils.utcnow()
        message = await channel.send(content=f'{client.mention} | {ticket_supp.mention}', embed=embed)
        thread = await message.create_thread(name=f"GFX-{client.name} private discussion", auto_archive_duration=60)

        db.exec(f'INSERT INTO orders (CHANNEL, CLIENT, ARTIST, PLACEMENT) VALUES (?, ?, ?, ?)', channel.id, client.id,
                0, datetime.datetime.now().strftime("%d / %m / %Y"))
        db.commit()

    @discord.ui.button(emoji='<:vfx:1064863743802081280>', style=discord.ButtonStyle.gray, custom_id='Gray:VFX')
    async def VFX_button(self, interaction=discord.Interaction, button=discord.ui.Button):
        artists = interaction.guild.get_role(cfg.ARTISTS)
        ticket_supp = interaction.guild.get_role(cfg.SUPPORT)
        client_role = interaction.guild.get_role(cfg.CLIENT)
        community = interaction.guild.get_role(cfg.COMMUNITY)

        client = interaction.user
        categ = discord.utils.get(interaction.guild.categories, id=cfg.ORDER_TICK)
        channel = await categ.create_text_channel(name=f'VFX-{client.name}')
        await channel.set_permissions(interaction.guild.default_role, view_channel=False)
        await channel.set_permissions(client, view_channel=True, send_messages=True)
        await channel.set_permissions(ticket_supp, view_channel=True, send_messages=True,
                                      send_messages_in_threads=False)
        await channel.set_permissions(artists, view_channel=True, send_messages=True, send_messages_in_threads=False)
        # await channel.set_permissions(client_role, view_channel=False)
        await channel.set_permissions(community, view_channel=False)

        embed = discord.Embed(title='VFX Ticket',
                              description=f'Ticket Opened by {client.mention}\nHelp will be with you shortly.\nCheck pricing and other information by using `%procedure`, `%price`, `%form`.',
                              color=cfg.CLR)
        embed.timestamp = discord.utils.utcnow()
        message = await channel.send(content=f'{client.mention} |', embed=embed)
        thread = await message.create_thread(name=f"VFX-{client.name} private discussion", auto_archive_duration=60)

        db.exec(f'INSERT INTO orders (CHANNEL, CLIENT, ARTIST, PLACEMENT) VALUES (?, ?, ?, ?)', channel.id, client.id,
                0, datetime.datetime.now().strftime("%d / %m / %Y"))
        db.commit()


class Orders(commands.Cog):
    """This COG handles with the different types of order commands"""

    def __init__(self, bot):
        self.bot = bot
        self.db = None
        self.bot.loop.create_task(self.connect_database())

    async def cog_load(self):
        self.bot.add_view(Buttons())

    async def connect_database(self):
        self.db = await aiosqlite.connect('/home/ubuntu/graphics-code-bott/points.db')

    @commands.command(name='OrderButton', hidden=True)
    @commands.has_permissions(administrator=True)
    async def order_button(self, ctx):
        """Sends Order Button."""
        embed = discord.Embed(title='Place Order', description=f"""⪦━━━━━━━━━━━━━━━━━━━━━━━⪧
               **ORDERING PANEL**

> For creating an order ticket, **__just click on either of the two buttons [GFX & VFX]__** corresponding to the type of design you want to order & **__a designated ticket will get created automatically__** by the bot. 

⪦━━━━━━━━━━━━━━━━━━━━━━━⪧""")
        embed.set_image(
            url="https://media.discordapp.net/attachments/1150321238997205002/1150359107346386985/order.png?width=1025&height=202")
        embed.colour = (cfg.CLR)
        embed.timestamp = discord.utils.utcnow()

        view = Buttons()

        msg = await ctx.send(embed=embed, view=view)
        print(msg.id)

    @commands.command(name='claim')
    async def claim_command(self, ctx):
        """```Claims an order. Only works in Ticket Channels.
        Can     only be claimed by users having <@&992651587577196686>.
        To override this command, administrator can user `assign` command to assign the project to another artist.```"""
        channels = db.column('SELECT CHANNEL FROM orders')
        if ctx.channel.id in channels:
            pass
        else:
            await ctx.send('This is not a ticket in my records.')
            return

        artist = db.field('SELECT ARTIST FROM orders WHERE CHANNEL = ?', ctx.channel.id)
        if artist == 0:
            pass
        else:
            await ctx.send(f'This order was already claimed by <@{artist}>', delete_after=10)
            return

        cursor = await self.db.cursor()
        await cursor.execute("SELECT * FROM points WHERE user_id = ?", (ctx.author.id,))
        res = await cursor.fetchone()
        if res is None:
            await cursor.execute("INSERT INTO points(user_id , points) VALUES(?,?)", (ctx.author.id, 0))

        artists = ctx.guild.get_role(cfg.ARTISTS)
        ticket_supp = ctx.guild.get_role(cfg.SUPPORT)
        client_role = ctx.guild.get_role(cfg.CLIENT)
        community = ctx.guild.get_role(cfg.COMMUNITY)

        if not artists in ctx.author.roles:
            await ctx.send('You are not an artist you cannot claim this order.')
            return

        embed = discord.Embed(title='Order Claimed.',
                              description=f'Your order in <#{ctx.channel.id}> was claimed by {ctx.author.mention}.',
                              color=cfg.CLR)
        embed.timestamp = discord.utils.utcnow()
        client_id = db.field('SELECT CLIENT FROM orders WHERE CHANNEL = ?', ctx.channel.id)
        client = ctx.guild.get_member(client_id)
        try:
            await client.send(embed=embed)
        except:
            pass

        await ctx.channel.set_permissions(ctx.author, view_channel=True, send_messages=True)
        await ctx.channel.set_permissions(artists, view_channel=False)
        await ctx.channel.set_permissions(ticket_supp, view_channel=False)

        db.exec(f'UPDATE orders SET ARTIST = ? WHERE CHANNEL = ? AND CLIENT = ?', ctx.author.id, ctx.channel.id,
                client_id)
        db.commit()

        await ctx.send(f'Successfully Claimed')

    @commands.command(name='unclaim')
    async def unclaim_ticket(self, ctx):
        """```Unclaims an order. Only works in Ticket Channels.
        Can only be unclaimed by the artist who claimed the ticket.
        To override the command, administrators can user `revoke` command to remove an artist from a project and assign another artist in case of unavailability of the artist.```"""
        channels = db.column('SELECT CHANNEL FROM orders')
        if ctx.channel.id in channels:
            pass
        else:
            await ctx.send('This is not a ticket in my records.')
            return

        artists = ctx.guild.get_role(cfg.ARTISTS)
        ticket_supp = ctx.guild.get_role(cfg.SUPPORT)
        client_role = ctx.guild.get_role(cfg.CLIENT)
        community = ctx.guild.get_role(cfg.COMMUNITY)

        artist_id = db.field('SELECT ARTIST FROM orders WHERE CHANNEL = ?', ctx.channel.id)
        if artist_id == 0:
            await ctx.send('This order was never claimed.', delete_after=10)
            return

        if not ctx.author.id == artist_id:
            await ctx.send('Only the Artist who claimed the Order can Unclaim it.', delete_after=10)
            return

        db.exec(f'UPDATE orders SET ARTIST = ? WHERE CHANNEL = ?', 0, ctx.channel.id)
        db.commit()

        embed = discord.Embed(title='Order Unclaimed.',
                              description=f'You successfully unclaimed this order, a new artist may now be assigned.',
                              color=cfg.CLR)
        embed.timestamp = discord.utils.utcnow()

        client_id = db.field('SELECT CLIENT FROM orders WHERE CHANNEL = ?', ctx.channel.id)
        client = ctx.guild.get_member(client_id)

        await ctx.send(embed=embed)
        await ctx.channel.edit(overwrites={})
        await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
        await ctx.channel.set_permissions(client, view_channel=True, send_messages=True)
        await ctx.channel.set_permissions(ticket_supp, view_channel=True, send_messages=True)
        await ctx.channel.set_permissions(artists, view_channel=True, send_messages=True)

        await ctx.channel.set_permissions(community, view_channel=False)

        await ctx.channel.send(content=f'{ticket_supp.mention} Please Assign another artist to **{client.name}**.')

    @commands.command(name='receipt', aliases=['reciept', 'complete'])
    async def complete_command(self, ctx):
        """```Complete an order and print the receipt for the same.
        **Note:** You will only have 300 seconds to submit the order details.```"""
        channels = db.column('SELECT CHANNEL FROM orders')
        if ctx.channel.id in channels:
            pass
        else:
            await ctx.send('This is not a ticket in my records.')
            return

        client_id, artist_id = db.record('SELECT CLIENT, ARTIST FROM orders WHERE CHANNEL = ?', ctx.channel.id)
        if artist_id == None or 0:
            await ctx.send(f'In my records, this Order was never claimed. Claim this order by `{ctx.prefix}claim`.')
            return

        artist = ctx.guild.get_member(artist_id)
        client = ctx.guild.get_member(client_id)

        embed = discord.Embed(title="Confirmation to continue",
                              description="Would you like to continue the receipt generating process?")
        await ctx.send(embed=embed, view=Receipt_Button())

    @commands.command(name='delete')
    async def close_channel(self, ctx):
        """```Deletes a Ticket Channel.```"""
        channels = db.column('SELECT CHANNEL FROM orders')
        if ctx.channel.id in channels:
            pass
        else:
            await ctx.send('This is not a ticket in my records.')
            return

        db.exec('DELETE FROM orders WHERE CHANNEL=?', ctx.channel.id)
        db.commit()
        self.transcript()
        await ctx.send('Deleting channel in 10 seconds.')
        await asyncio.sleep(10)
        await ctx.channel.delete()

    @commands.command(name='transcript')
    async def transcript(ctx, ticket_channel: discord.TextChannel):
        "```Generates Transcript of an Order Ticket```"
        member = ctx.guild.get_member(ctx.author.id)

        # Check if the user has the necessary permissions to read messages in the specified ticket channel
        if not member.guild_permissions.read_messages:
            await ctx.send("You don't have permission to read messages in that ticket channel.")
            return

        # Fetch messages from the ticket channel
        messages = await ticket_channel.history(limit=None).flatten()

        # Create a Markdown transcript content with message details
        transcript_content = ""
        for message in messages:
            timestamp = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
            author_name = message.author.display_name
            content = message.content
            transcript_content += f"**[{timestamp}] [{author_name}]**: {content}\n"

        # Send the transcript content to a specific channel
        transcript_channel = ctx.guild.get_channel(cfg.TRANSCRIPTS)  # Replace with your channel ID
        if transcript_channel is None:
            await ctx.send("Transcript channel not found.")
            return

        await transcript_channel.send(f"Transcript for {ticket_channel.mention}:\n\n{transcript_content}")
        await ctx.send("Transcript sent to the designated channel.")

    @commands.command(name='assign')
    @commands.has_permissions(administrator=True)
    async def assign_artist(self, ctx, artist: discord.Member):
        """```Assigns a Ticket to an artist.```"""
        channels = db.column('SELECT CHANNEL FROM orders')
        if ctx.channel.id in channels:
            pass
        else:
            await ctx.send(
                f'This is not a ticket in my records. First run `{ctx.prefix}addc <client>` to add this channel as a ticket.')
            return

        already = db.field('SELECT ARTIST FROM orders WHERE CHANNEL = ?', ctx.channel.id)
        if already == 0:
            pass
        else:
            await ctx.send(
                f'This channel is already assigned to **<@{already}>**. First run `{ctx.prefix}revoke` to revoke this ticket from the artist.')
            return

        artists = ctx.guild.get_role(cfg.ARTISTS)
        if not artists in artist.roles:
            await ctx.send('This user is not an artist')
            return

        db.exec('UPDATE orders SET ARTIST = ? WHERE CHANNEL = ?', artist.id, ctx.channel.id)
        db.commit()

        ticket_supp = ctx.guild.get_role(cfg.SUPPORT)

        await ctx.channel.set_permissions(artist, view_channel=True, send_messages=True)
        await ctx.channel.set_permissions(artists, view_channel=False)
        await ctx.channel.set_permissions(ticket_supp, view_channel=False)

        await ctx.send(f'Successfully assigned this order to {artist.mention}')

    @commands.command(name='revoke')
    @commands.has_permissions(administrator=True)
    async def revoke_ticket(self, ctx):
        """```Take away an order from an artist.```"""
        channels = db.column('SELECT CHANNEL FROM orders')
        if ctx.channel.id in channels:
            pass
        else:
            await ctx.send('This is not a ticket in my records.')
            return

        artist = db.field('SELECT ARTIST FROM orders WHERE CHANNEL = ?', ctx.channel.id)
        if artist == 0:
            await ctx.send('This Ticket was never claimed.')
            return

        db.exec('UPDATE orders SET ARTIST = ? WHERE CHANNEL = ?', 0, ctx.channel.id)
        db.commit()

        client = db.field('SELECT CLIENT FROM orders WHERE CHANNEL = ?', ctx.channel.id)
        client = ctx.guild.get_member(client)

        artists = ctx.guild.get_role(cfg.ARTISTS)
        ticket_supp = ctx.guild.get_role(cfg.SUPPORT)
        client_role = ctx.guild.get_role(cfg.CLIENT)
        community = ctx.guild.get_role(cfg.COMMUNITY)

        await ctx.channel.edit(overwrites={})
        await ctx.channel.set_permissions(ctx.guild.default_role, view_channel=False)
        await ctx.channel.set_permissions(client, view_channel=True, send_messages=True)
        await ctx.channel.set_permissions(ticket_supp, view_channel=True, send_messages=True)
        await ctx.channel.set_permissions(artists, view_channel=True, send_messages=True)

        await ctx.channel.set_permissions(community, view_channel=False)

        await ctx.send(f'Successfully revoked from <@{artist}>')

    @commands.command(name='addc')
    async def add_channel_to_db(self, ctx, client: discord.Member):
        """```Adds a non-ticket/non-registered channel as a ticket.```"""
        channels = db.column('SELECT CHANNEL FROM orders')
        if ctx.channel.id in channels:
            await ctx.send('This channel is alrady a Ticket.')
            return
        else:
            pass

        artists = ctx.guild.get_role(cfg.ARTISTS)
        if not artists in ctx.author.roles:
            await ctx.send('You are not an artist, you cannot execute this comamnd.')
            return

        db.exec('INSERT INTO orders (CLIENT, CHANNEL) VALUES (?, ?)', client.id, ctx.channel.id)
        db.commit()
        await ctx.send(f'Channel Successfully added as Ticket with client marked as **{client.name}**.')

    @commands.command()
    async def procedure(self, ctx):
        """```Displays the procedure to place an order.```"""
        description = (f'Step 1: Open a ticket from <#992660626272964629>\n'
                       f'In the ticket channel explain your order to the artist in the format given in `%form`.\n'
                       f'Wait for an artist to claim your Order. Once an artist claims your order, you will be notified in your DMs.\n'
                       f'After an artist has claimed your order, he/she will complete your order and notify you.\n'
                       f'In order to cancel your order, you can click **[Cancel]** Button at any point in time and the artists will be notified.\n'
                       f'In case the artist is unable to Complete your order, he/she will **[Unclaim]** your order and you need to wait till another artist accepts your request.\n'
                       f'In case of incompatibiliy, the artists may **[Reject]** your order and the ticket will be closed.')
        embed = discord.Embed(title='Procedure', description=description, color=cfg.CLR)
        embed.set_image(url="https://media.discordapp.net/attachments/1150321238997205002/1150359106473951342/store.png?width=1025&height=202")
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(text=f'Requested by {ctx.author.name} | {ctx.author.id}')
        await ctx.send(embed=embed)

    @commands.command()
    async def price(self, ctx):
        """```Displays the rough pricing for varity of work styles.```"""
        embed = discord.Embed(color=(cfg.CLR))
        embed.description = ("""## GRAPHICS CODE FX STORE
⪦━━━━━━━━━━━━━━━━━━━━━━━⪧

                  <:red_dot:1150768677294194730>**Graphic Designs**<:red_dot:1150768677294194730>

<a:fancyarr:1064443589825933343> **__PROFILE PICTURE__ [2$ - 10$]**
<a:fancyarr:1064443589825933343> **__CONCEPT LOGO__ [8$]**
<a:fancyarr:1064443589825933343> **__LOGO DESIGN__ [4$ - 10$]**
<a:fancyarr:1064443589825933343> **__BANNER__ [3$]**
<a:fancyarr:1064443589825933343> **__HEADER__ [5$]**
<a:fancyarr:1064443589825933343> **__POSTER__ [4$]**
<a:fancyarr:1064443589825933343> **__ROSTER__ [6$]**
<a:fancyarr:1064443589825933343> **__PRE-MADE MASCOT__ [3$]**
<a:fancyarr:1064443589825933343> **__CUSTOM MASCOT__ [6$]**
<a:fancyarr:1064443589825933343> **__VECTOR__ [12$]**
<a:fancyarr:1064443589825933343> **__THUMBNAIL__ [5$]**
<a:fancyarr:1064443589825933343> **__STATIC OVERLAY__ [3$]** 
<a:fancyarr:1064443589825933343> **__REVAMP__ [20$]**

⪦━━━━━━━━━━━━━━━━━━━━━━━⪧

              <:red_dot:1150768677294194730>**Visual Effect Designs**<:red_dot:1150768677294194730>

<:red_dot:1150768677294194730> **__ANIMATED LOGO/GIF__ [6$]**
<:red_dot:1150768677294194730> **__ANIMATED OVERLAY__ [4$]**
<:red_dot:1150768677294194730> **__INTRO__ [8$]**
<:red_dot:1150768677294194730> **__OUTRO__ [8$]**
<:red_dot:1150768677294194730> **__MONTAGE/EDIT__ [6$ PER 60 SEC]**

⪦━━━━━━━━━━━━━━━━━━━━━━━⪧
⪦━━━━━━━━━━━━━━━━━━━━━━━⪧

       <:red_dot:1150768677294194730>**Payment Methods Accepted**<:red_dot:1150768677294194730>

<a:fancyarr:1064443589825933343> **__PAYTM__ <:paytm:1064445815688544258>**
<a:fancyarr:1064443589825933343> **__GOOGLE PAY__ <:gpay:1064445864598323200>**
<a:fancyarr:1064443589825933343> **__FAMPAY__ <:fampay:1064445925189222521>**
<a:fancyarr:1064443589825933343> **__UNIFIED PAYMENTS INTERFACE__ <:upi:1064446375997227009>**
<a:fancyarr:1064443589825933343> **__PAYPAL__ <:paypal:1064445964519223316>**
<a:fancyarr:1064443589825933343> **__NITRO__ <a:nitro:1064446026200649789>**
<a:fancyarr:1064443589825933343> **__NITRO CLASSIC__ <a:nitroclassic:853221718158999562>**
<a:fancyarr:1064443589825933343> **__GIFTCARD__ <:giftcard:1064446574501056583>**

⪦━━━━━━━━━━━━━━━━━━━━━━━⪧

                <:red_dot:1150768677294194730>**Things to be Noted**<:red_dot:1150768677294194730>

<a:fancyarr:1064443589825933343>  **__NOTE - 1__**
> Use slash command /payment to get the list of payment methods being accepted at the moment.
<a:fancyarr:1064443589825933343>  **__NOTE - 2__**
> Pricing of design depends on the complexity of the order, time being invested to provide the best design, assets/resources needed to fulfill the needs of the client & other basic things. Therefore, the pricing mentioned above in the list is just an estimate/approximate value. The list doesn't not conclude the final pricing.

⪦━━━━━━━━━━━━━━━━━━━━━━━⪧""")
        embed.set_image(
            url="https://media.discordapp.net/attachments/1150321238997205002/1150359775993925673/pricing.png?width=1025&height=202")
        await ctx.send(embed=embed)

    @commands.command()
    async def oldform(self, ctx):
        """```Displays the form for placing an order.```"""
        embed = discord.Embed(title='Order Form', description=f"""1) What Are You Ordering.
2) Colour Theme.
3) Example Of the What You Are Ordering.
4) Payment Method - Paid / Invites / Booster.
5) Deadline. """, color=discord.Color(0x2F3136))
        embed.set_footer(text=f'{ctx.guild.name} | {ctx.guild.id}')
        embed.timestamp = discord.utils.utcnow()
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
        embed.set_image(
            url="https://media.discordapp.net/attachments/1150321238997205002/1150359107677728819/form.png?width=1025&height=202")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Orders(bot))
