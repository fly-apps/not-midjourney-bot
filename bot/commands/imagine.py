import os
import time
import asyncio
import discord
from sqids import Sqids
from discord.ext import commands
from discord.commands import Option
from api_client import APIClient
import logging

logging.basicConfig(level=logging.INFO)

client = APIClient(os.getenv("URL"))

# Initialize the bot instance with intents if needed
intents = discord.Intents.default()
bot = commands.Bot(intents=intents)


class Imagine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.running = False
        self.sqids = Sqids()

    available_styles = client.all_styles()

    available_aspect_ratios = [
        "704×1408",
        "704×1344",
        "768×1344",
        "768×1280",
        "832×1216",
        "832×1152",
        "896×1152",
        "896×1088",
        "960×1088",
        "960×1024",
        "1024×1024",
        "1024×960",
        "1088×960",
        "1088×896",
        "1152×896",
        "1152×832",
        "1216×832",
        "1280×768",
        "1344×768",
        "1344×704",
        "1408×704",
        "1472×704",
        "1536×640",
        "1600×640",
        "1664×576",
        "1728×576",
    ]

    @bot.slash_command(name="imagine", description="Generate an image from text")
    async def imagine(
        self,
        ctx: discord.ApplicationContext,
        prompt: Option(str, "Your prompt for the image to generate", required=True),
        style1: Option(
            str,
            "The styles to use in the image generation",
            autocomplete=discord.utils.basic_autocomplete(available_styles),
            required=False,
        ),
        style2: Option(
            str,
            "The styles to use in the image generation",
            autocomplete=discord.utils.basic_autocomplete(available_styles),
            required=False,
        ),
        style3: Option(
            str,
            "The styles to use in the image generation",
            autocomplete=discord.utils.basic_autocomplete(available_styles),
            required=False,
        ),
        quality: Option(
            bool,
            "Set to true to run at Quality instead of Speed",
            required=False,
            default=False,
        ),
        ar: Option(
            str,
            "The aspect ratio to use for the image",
            autocomplete=discord.utils.basic_autocomplete(available_aspect_ratios),
            required=False,
        ),
        negative: Option(str, "Negative prompt for the image", required=False),
    ):
        # Collect the styles from style1, style2, and style3 and combine them into a list
        style_list = [style for style in (style1, style2, style3) if style is not None]

        # Check if any of the styles are set
        if style_list:
            # Use the styles provided by the user
            style_selections = style_list
        else:
            # Use some default styles
            style_selections = ["Fooocus Enhance", "Fooocus Sharp"]

        # Always add 'Fooocus V2' to the style selections
        style_selections.append("Fooocus V2")

        if self.running:
            await ctx.respond("Error: Already running")
            return
        self.running = True

        # Defer response as image generation is async
        await ctx.response.defer()
        try:
            # Prepare the request dictionary for the text_to_image API call
            text2img_request = {
                "prompt": prompt,
                "negative_prompt": negative if negative else "",
                "style_selections": style_selections,
                "performance_selection": "Quality" if quality else "Speed",
                "aspect_ratios_selection": ar if ar else "1152×896",
                "image_number": 1,
                # "image_seed": int(seed_custom) if seed_custom.isdigit() else -1,  # Convert seed_custom to int or use -1
                "image_seed": -1,
                "sharpness": 2,
                "guidance_scale": 4,
                "base_model_name": "juggernautXL_version6Rundiffusion.safetensors",
                "refiner_model_name": "None",
                "refiner_switch": 0.5,
                "loras": [
                    {
                        "model_name": "sd_xl_offset_example-lora_1.0.safetensors",
                        "weight": 0.1,
                    }
                ],
                "advanced_params": {
                    "disable_preview": False,
                    "adm_scaler_positive": 1.5,
                    "adm_scaler_negative": 0.8,
                    "adm_scaler_end": 0.3,
                    "refiner_swap_method": "joint",
                    "adaptive_cfg": 7,
                    "sampler_name": "dpmpp_2m_sde_gpu",
                    "scheduler_name": "karras",
                    "overwrite_step": -1,
                    "overwrite_switch": -1,
                    "overwrite_width": -1,
                    "overwrite_height": -1,
                    "overwrite_vary_strength": -1,
                    "overwrite_upscale_strength": -1,
                    "mixing_image_prompt_and_vary_upscale": False,
                    "mixing_image_prompt_and_inpaint": False,
                    "debugging_cn_preprocessor": False,
                    "skipping_cn_preprocessor": False,
                    "controlnet_softness": 0.25,
                    "canny_low_threshold": 64,
                    "canny_high_threshold": 128,
                    "freeu_enabled": False,
                    "freeu_b1": 1.01,
                    "freeu_b2": 1.02,
                    "freeu_s1": 0.99,
                    "freeu_s2": 0.95,
                    "debugging_inpaint_preprocessor": False,
                    "inpaint_disable_initial_latent": False,
                    "inpaint_engine": "v1",
                    "inpaint_strength": 1,
                    "inpaint_respective_field": 1,
                },
                "require_base64": False,
                "async_process": False,
            }

            # Generate a unique ID using Sqids
            unique_id = self.sqids.encode(
                [ctx.author.id, int(time.time())]
            )  # Use author ID and current time for uniqueness to avoid fs conflicts

            # Use the unique ID for the filename
            result_filename = f"result_{unique_id}.png"

            # Call the new text_to_image API
            result = client.text_to_image(text2img_request, accept="image/png")

            # Save the result to a file with the unique filename
            with open(result_filename, "wb") as f:
                f.write(result)

            # Wait for the result file to be available
            while not os.path.exists(result_filename):
                await asyncio.sleep(1)

            with open(result_filename, "rb") as f:
                await ctx.respond(
                    "**" + prompt + "**", file=discord.File(f, result_filename)
                )

            # Optionally, delete the file after sending it
            os.remove(result_filename)

        except Exception as e:
            # Handle exceptions and return an error message
            await ctx.respond(f"An error occurred while generating the image: {e}")
        finally:
            self.running = False


def setup(bot):
    bot.add_cog(Imagine(bot))
