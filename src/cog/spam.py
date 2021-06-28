from discord.ext import commands

from bot import config


class Spam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        if message.author is self.bot.user:
            return

        for word in config["spam"]:
            if word in message.content:
                await message.add_reaction(config["arch-emoji"])
                await message.channel.send("Bloeckchengrafik#0420 uses arch btw")
                return


def setup(bot):
    bot.add_cog(Spam(bot))
