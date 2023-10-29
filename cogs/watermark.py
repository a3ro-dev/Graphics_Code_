import discord
from discord.ext import commands
from PIL import Image
import requests
from io import BytesIO
import concurrent.futures
import time

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

        # Function to apply watermark and collect diagnostic details
        def apply_watermark(image):
            watermark = Image.open("assets/wm.png")
            watermark_reso = watermark.size
            image_reso = image.size

            start_time = time.time()
            # Apply the watermark
            try:
                input_width, input_height = image.size
                watermark = watermark.resize((input_width // 1.5, input_height // 1.5))

                watermark_width, watermark_height = watermark.size
                paste_x = (input_width - watermark_width) // 2
                paste_y = (input_height - watermark_height) // 2

                transparent = Image.new('RGBA', (input_width, input_height), (0, 0, 0, 0))
                transparent.paste(watermark, (paste_x, paste_y), watermark)

                watermarked_image = Image.alpha_composite(image.convert("RGBA"), transparent)
                watermarked_image = watermarked_image.convert("RGB")

                # Save the watermarked image
                watermarked_image.save("watermarked_image.png")
                watermark_time = time.time() - start_time

                return watermarked_image, watermark_reso, image_reso, watermark_time
            except Exception as e:
                return f"An error occurred: {e}", watermark_reso, image_reso, 0

        # Fetch the image and process with threading
        if image_link:
            response = requests.get(image_link, stream=True)
            if response.status_code != 200:
                await ctx.send("Failed to fetch the image from the provided link.")
                return
            image_data = BytesIO()
            for chunk in response.iter_content(chunk_size=1024):
                image_data.write(chunk)
            image_data.seek(0)
            image = Image.open(image_data)
        else:
            attachment = ctx.message.attachments[0]
            image_data = BytesIO(await attachment.read())
            image = Image.open(image_data)

        diagnostic_embed = discord.Embed(title="Watermark Diagnostics", color=0x7289DA)
        
        try:
            with concurrent.futures.ThreadPoolExecutor() as executor:
                result = await self.bot.loop.run_in_executor(executor, apply_watermark, image)
            
            watermarked_image, watermark_reso, image_reso, watermark_time = result

            diagnostic_embed.add_field(name="Watermark Resolution", value=str(watermark_reso))
            diagnostic_embed.add_field(name="Image Resolution", value=str(image_reso))
            diagnostic_embed.add_field(name="Watermark Application Time", value=f"{watermark_time:.3f} seconds")

            img_byte_array = BytesIO()
            watermarked_image.save(img_byte_array, format='PNG')
            img_byte_array.seek(0)

            await ctx.send(embed=diagnostic_embed, file=discord.File(img_byte_array, filename="watermarked_image.png"))

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(Watermark(bot))
