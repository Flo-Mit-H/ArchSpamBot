import asyncio
import json
import logging
import os

import discord
from discord.ext import commands

# Initialize and Read the Config File
if not os.path.isfile("../config/config.json"):
    with open("../config/config.json", "w") as f:
        json.dump({
            "prefix": "!",
            "debug": True
        }, f, indent=4)
config = json.load(open("../config/config.json"))

# Initialize Bot Instance
bot = commands.Bot(command_prefix=config["prefix"], activity=discord.Activity(type=discord.ActivityType.listening, name="your linux messages"))


class Application:
    __cogs = [
        "spam"
    ]

    def __init__(self, discord_bot, bot_token):
        self.bot: commands.Bot = discord_bot
        self.logger = logging.getLogger("main")
        self.logger.setLevel(logging.DEBUG if config["debug"] else logging.INFO)

        self.load_extensions()

        @self.bot.event
        async def on_ready():
            # Bot Startup Logic
            self.logger.info(f"Logged in as {self.bot.user.name}#{self.bot.user.discriminator}")
            self.logger.debug("Initializing Update Task")
            bot.loop.create_task(self.update_task())
            self.logger.info("Initialized Update Task")

        # Run the Bot
        self.bot.run(bot_token)

    def load_extensions(self):
        for extension in self.__cogs:
            self.logger.debug(f"Loading Extension {extension}")
            __import__(f"cog.{extension}", fromlist=["setup"]).setup(bot)
            self.logger.info(f"Loaded Extension {extension}")
        self.logger.info(f"Loaded {len(self.__cogs)} Extensions in total")

    @staticmethod
    async def update_task():
        while True:
            bot.command_prefix = config["prefix"]
            await asyncio.sleep(1)


logging.basicConfig(
    level=logging.DEBUG if config["debug"] else logging.INFO,
    format='(%(asctime)s) %(levelname)7s - %(name)20s: %(message)s'
)

token = open("../token.txt", "r", encoding="utf-8").read()
if __name__ == "__main__":
    Application(bot, token)
