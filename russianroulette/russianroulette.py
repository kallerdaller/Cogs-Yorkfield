import discord
from discord.ext import commands

class Mycog:
    """Russian Roulette"""
    
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_contect=True, aliases=["rr", "russian"])
    async def russianroulette(self, ctx, type):
        """This does stuff!"""
        
        #Your code will go here
        user = ctx.message.author
        bank = self.bot.get_cog("Economy").bank
        await self.bot.say("I can do stuff!")
        
def setup(bot):
    bot.add_cog(Mycog(bot))
