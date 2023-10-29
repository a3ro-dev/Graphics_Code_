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

        # Maximum allowed file size in bytes
        MAX_FILE_SIZE = 8 * 1024 * 1024  # 8 MB

        # Check if an image link or an attachment is provided
        if not image_link and len(ctx.message.attachments) == 0:
            await ctx.send("Please upload an image or provide an image link.")
            return

        # Define a function to process the watermark and image
        async def process_image(image):
            try:
                # Open the image and the watermark
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

                # Convert the watermarked image into bytes
                img_byte_array = BytesIO()
                watermarked_image.save(img_byte_array, format='PNG')
                img_byte_array.seek(0)

                # Send the watermarked image in the chat
                await ctx.send(file=discord.File(img_byte_array, filename="watermarked_image.png"))

            except Exception as e:
                await ctx.send(f"An error occurred: {e}")

        # If an image link is provided, fetch the image using the link
        if image_link:
            response = requests.get(image_link)
            if response.status_code != 200:
                await ctx.send("Failed to fetch the image from the provided link.")
                return
            if int(response.headers.get('content-length', 0)) > MAX_FILE_SIZE:
                await ctx.send("The file size exceeds the maximum allowed limit.")
                return
            image_data = BytesIO(response.content)
            image = Image.open(image_data)
            await process_image(image)
        else:
            # If an image is uploaded, retrieve the attachment
            attachment = ctx.message.attachments[0]
            if attachment.size > MAX_FILE_SIZE:
                await ctx.send("The file size exceeds the maximum allowed limit.")
                return
            image_data = BytesIO(await attachment.read())
            image = Image.open(image_data)
            await process_image(image)

async def setup(bot):
    await bot.add_cog(Watermark(bot))
