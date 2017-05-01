import discord
from discord.ext import commands
from discord.permissions import Permissions

class EventBets:
    """Create an event which people can bet on"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True, aliases=["be"])
    async def betevent(self):
        """Create event"""

        #Your code will go here
        user = ctx.message.author
        await self.bot.say("Event name?")
        print(user.roles)

def setup(bot):
    n = EventBets(bot)
    bot.add_cog(n)
#308553548566757378
