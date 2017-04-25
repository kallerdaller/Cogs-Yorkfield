import discord
from discord.ext import commands

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meh(self, user : discord.Member):
        """This does stuff!"""

        #Your code will go here
        await self.bot.say("Meh " + user.mention)

def setup(bot):
    bot.add_cog(Mycog(bot))
