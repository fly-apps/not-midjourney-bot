import os
import discord
import logging

logging.basicConfig(level=logging.INFO)

# Load environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
if not DISCORD_TOKEN:
    raise ValueError("No DISCORD_TOKEN found in environment variables")

# Define intents
intents = discord.Intents.default()
intents.message_content = True

# Create a new bot instance with the specified intents
bot = discord.Bot(intents=intents)

# Function to load extensions
def load_extensions():
    commands_path = os.path.abspath('./commands')  # Get an absolute path to the commands folder
    for filename in os.listdir(commands_path):
        if filename.endswith('.py') and not filename.startswith('_'):
            extension = f'commands.{filename[:-3]}'
            try:
                bot.load_extension(extension)
                print(f'Loaded extension: {extension}')
            except Exception as e:
                print(f'Failed to load extension {extension}: {e}')

# Load commands from the commands folder before starting the bot
load_extensions()

# Event to confirm the bot has logged in
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# Run the bot
bot.run(DISCORD_TOKEN)
