import discord
from discord.ext import commands
from discord.permissions import Permissions
from .utils import checks
import asyncio
from .utils.dataIO import dataIO

class EventBets:
    """Create an event which people can bet on"""

    def __init__(self, bot):
        self.bot = bot
        self.file_path = "data/irlbetting/irlbetting.json"
        self.json_data = dataIO.load_json(self.file_path) 

    @commands.command(pass_context=True, aliases=["be"])
    @checks.admin_or_permissions(manage_server=True)
    async def betevent(self, ctx):
        """Create event"""

        #Your code will go here
        user = ctx.message.author
        await self.bot.say("Event name?")
        eventname = await self.bot.wait_for_message(timeout=30, author=user)
        eventname = str(answer.content)
        if answer is None:
            await self.bot.say("You didn't enter anything. Event cancelled")
            return
        await self.bot.say("Event name: " + eventname)
        

def check_folders():
    if not os.path.exists("data/irlbetting"): 
        print("Creating data/irlbetting floder...")  
        os.makedirs("data/irlbetting") 

        
def check_files(): 
    system = {"Events": {"1": {"Name": "",
                               "Multiplier": 1,
                               "Users": { "1": {"Bet": 0,
                                                "Choice": ""},
                                        },
                               "Date": {"Hour": 0,
                                        "Day": 0,
                                        "Month": 0},
                               "Outcomes": {"1": ""}}}}
                         
    f = "data/irlbetting/irlbetting.json"
    if not dataIO.is_valid_json(f):
        print("Creating defualt irlbetting.json...")
        dataIO.save_json(f, system)
        
        
def setup(bot):
    check_folders()
    check_files()
    n = EventBets(bot)
    bot.add_cog(n)
