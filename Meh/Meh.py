import discord
from discord.ext import commands

class Mycog:
    """Tells a user that you said meh"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def meh(self, ctx, user : discord.Member):
        """Tags a person and tells them meh"""

        #Your code will go here
        author = ctx.message.author
        author.id # This is your user id number
        user.id # This is the discord member's id
        author.name # this is the user's id
        user.name # This is the discord member's name
        await self.bot.say(user.mention + ", " + "says 'Meh'" + author.id)

def setup(bot):
    bot.add_cog(Mycog(bot))
