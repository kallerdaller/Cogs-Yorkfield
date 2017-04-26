import discord
from discord.ext import commands

class Mycog:
    """Tells a user that you said meh"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def meh(self, ctx, user : discord.Member):
        """Tags a person and tells them meh"""

        #Your code will go here
        author = ctx.message.author
        await self.bot.say(user.mention + ", " + "says 'Meh'" + author.mention)

def setup(bot):
    bot.add_cog(Mycog(bot))
