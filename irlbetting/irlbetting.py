import discord
from discord.ext import commands

class Mycog:
    """My custom cog that does stuff!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True, aliases=["be"])
    async def betevent(self):
        """Create event"""

        #Your code will go here
        await self.bot.say("Event name?")

def setup(bot):
    n = EventBets(bot)
    bot.add_cog(n)
