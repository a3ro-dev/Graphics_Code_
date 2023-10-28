import discord
from discord.ext import commands
from PIL import Image
import requests
from io import BytesIO

class Watermark(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def watermark(self, ctx, image_link: str = None):
        """
        Apply a watermark to an uploaded image or an image from a provided link.

        Parameters:
        - ctx (commands.Context): The context of the command invocation.
        - image_link (str): Optional. The link to an image for watermarking.

        The command checks for uploaded images or provided links. It fetches the image and applies a watermark.
        """

        # Check if an image link or an attachment is provided
        if not image_link and len(ctx.message.attachments) == 0:
            await ctx.send("Please upload an image or provide an image link.")
            return

        # If an image link is provided, fetch the image using the link
        if image_link:
            response = requests.get(image_link)
            if response.status_code != 200:
                await ctx.send("Failed to fetch the image from the provided link.")
                return
            image_data = BytesIO(response.content)
        else:
            # If an image is uploaded, retrieve the attachment
            attachment = ctx.message.attachments[0]
            image_data = BytesIO(await attachment.read())

        try:
            # Open the image and the watermark
            image = Image.open(image_data)
            watermark = Image.open("assets/wm.png")

            # Get image dimensions and calculate the watermark size based on the shorter side
            input_width, input_height = image.size
            min_dimension = min(input_width, input_height)

            # Calculate the scaling ratio for the watermark
            scale_factor = min_dimension / 10  # Define a scale factor (you can adjust this value)

            # Resize the watermark based on the scale factor
            new_width = int(watermark.width * scale_factor)
            new_height = int(watermark.height * scale_factor)
            watermark = watermark.resize((new_width, new_height))

            # Calculate the position to paste the watermark at the center
            paste_x = (input_width - new_width) // 2
            paste_y = (input_height - new_height) // 2

            # Create a transparent layer to paste the watermark onto
            transparent = Image.new('RGBA', (input_width, input_height), (0, 0, 0, 0))
            transparent.paste(watermark, (paste_x, paste_y), watermark)

            # Apply watermark on the image
            watermarked_image = Image.alpha_composite(image.convert("RGBA"), transparent)
            watermarked_image = watermarked_image.convert("RGB")

            # Save the watermarked image and send it in the chat
            watermarked_image.save("watermarked_image.png")
            await ctx.send(file=discord.File("watermarked_image.png"))

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(Watermark(bot))
