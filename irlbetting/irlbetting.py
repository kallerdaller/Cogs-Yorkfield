import discord
from discord.ext import commands
from discord.permissions import Permissions

class EventBets:
    """Create an event which people can bet on"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, aliases=["be"])
    @checks.admin_or_permissions(manage_server=True)
    async def betevent(self, ctx):
        """Create event"""

        #Your code will go here
        user = ctx.message.author
        await self.bot.say("Event name?")

def setup(bot):
    n = EventBets(bot)
    bot.add_cog(n)
