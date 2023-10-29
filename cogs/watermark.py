import discord
from discord.ext import commands
from PIL import Image
import requests
from io import BytesIO
import concurrent.futures

class Watermark(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def watermark(self, ctx, image_link: str = None):
        MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB

        # Function to apply watermark on an image
        def apply_watermark(image):
            try:
                watermark = Image.open("assets/wm.png")

                input_width, input_height = image.size

                # Calculate watermark size based on the shorter side
                min_dimension = min(input_width, input_height)
                scale_factor = min_dimension / 10  # Define a scale factor (you can adjust this value)
                new_width = int(watermark.width * scale_factor)
                new_height = int(watermark.height * scale_factor)
                watermark = watermark.resize((new_width, new_height))

                # Calculate the position to paste the watermark at the center
                paste_x = (input_width - new_width) // 2
                paste_y = (input_height - new_height) // 2

                transparent = Image.new('RGBA', (input_width, input_height), (0, 0, 0, 0))
                transparent.paste(watermark, (paste_x, paste_y), watermark)

                watermarked_image = Image.alpha_composite(image.convert("RGBA"), transparent)
                watermarked_image = watermarked_image.convert("RGB")

                return watermarked_image

            except Exception as e:
                return f"An error occurred: {e}"

        async def process_image(image):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                watermarked_image = await self.bot.loop.run_in_executor(executor, apply_watermark, image)

            if isinstance(watermarked_image, str):
                await ctx.send(watermarked_image)
                return

            img_byte_array = BytesIO()
            watermarked_image.save(img_byte_array, format='PNG')
            img_byte_array.seek(0)
            await ctx.send(file=discord.File(img_byte_array, filename="watermarked_image.png"))

        # Fetch and process the image
        if image_link:
            response = requests.get(image_link, stream=True)
            if response.status_code != 200:
                await ctx.send("Failed to fetch the image from the provided link.")
                return
            content_length = response.headers.get('content-length')
            if content_length and int(content_length) > MAX_FILE_SIZE:
                await ctx.send("The file size exceeds the maximum allowed limit.")
                return
            image_data = BytesIO()
            for chunk in response.iter_content(chunk_size=1024):
                image_data.write(chunk)
            image_data.seek(0)
            image = Image.open(image_data)
            await process_image(image)
        else:
            attachment = ctx.message.attachments[0]
            if attachment.size > MAX_FILE_SIZE:
                await ctx.send("The file size exceeds the maximum allowed limit.")
                return
            image_data = BytesIO(await attachment.read())
            image = Image.open(image_data)
            await process_image(image)

async def setup(bot):
    await bot.add_cog(Watermark(bot))
