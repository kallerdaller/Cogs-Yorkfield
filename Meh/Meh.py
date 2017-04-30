import discord
from discord.ext import commands

class Meh:
    """Tells a user that you said meh"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def meh(self, ctx, user : discord.Member):
        """Tags a person and tells them meh"""

        #Your code will go here
        message = ctx.message
        await self.bot.delete_message(message)
        author = ctx.message.author
        await self.bot.say("Hey, " + user.mention + "!! " + author.mention + " wanted to tell you 'Meh'")

def setup(bot):
    n = Meh(bot)
    bot.add_cog(n)
