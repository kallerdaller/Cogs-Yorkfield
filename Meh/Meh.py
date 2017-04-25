import discord
from discord.ext import commands

class Mycog:
    """Tells a user that you said meh"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meh(self, user : discord.Member, discord.message):
        """Tags a person and tells them meh"""

        #Your code will go here
        delete_message(message)
        await self.bot.say("Meh " + user.mention)

def setup(bot):
    bot.add_cog(Mycog(bot))
