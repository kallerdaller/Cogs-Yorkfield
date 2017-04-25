import discord
from discord.ext import commands

class Mycog:
    """Tells a user that you said meh"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meh(self, user : discord.Member):
        """Tags a person and tells them meh"""

        #Your code will go here
        await self.bot.say(user.mention + "says 'Meh'")

def setup(bot):
    bot.add_cog(Mycog(bot))
