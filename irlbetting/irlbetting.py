import discord
from discord.ext import commands
from discord.permissions import Permissions
from .utils import checks
import asyncio
from .utils.dataIO import dataIO
import os

client = discord.Client()

class EventBets:
    """Create an event which people can bet on"""

    def __init__(self, bot):
        self.bot = bot
        self.file_path = "data/irlbetting/irlbetting.json"
        self.json_data = dataIO.load_json(self.file_path) 

    @commands.command(pass_context=True, aliases=["ce"])
    @checks.admin_or_permissions(manage_server=True)
    @client.event
    async def createevent(self, ctx):
        """Create event"""

        #Your code will go here
        user = ctx.message.author
        await self.bot.say("What is the name of the event?")
        eventname = await self.bot.wait_for_message(timeout=30, author=user)
        if eventname is None:
            await self.bot.say("You didn't enter anything. Event cancelled")
            return
        eventname = str(eventname.content)
        await self.bot.say("Event name: \n" + eventname)
        await self.bot.say("What are the possible outcomes of the event? You must have atleast 2. To stop inputting outcomes simply type `.`")
        a = 0
        outcome = []
        message = ""
        while not message == ".":
            await self.bot.say(str(a+1) + ": ")
            outcome.append(await self.bot.wait_for_message(timeout=30, author=user))
            if outcome[a] is None:
                if a == 3:
                    message = "."
                else:
                    await self.bot.say("You didn't enter anything. Event cancelled")
                    return
            else:
                outcome[a] = str(outcome[a].content)
                message = outcome[a]
            a += 1
        if len(outcome) < 2:
            return
        await self.bot.say("Outcomes: ")
        i = 0
        while i < a-1:
            await self.bot.say(outcome[i])
            i += 1
        await self.bot.say("What should the payout multiplier be?")
        payoutM = await self.bot.wait_for_message(timeout=30, author=user)
        if payoutM is None:
            await self.bot.say("You didn't enter anything. Event cancelled")
            return
        try:
            payoutM = int(payoutM.content)
        except ValueError:
            await self.bot.say("You must enter a number. Event cancelled")
            return
        await self.bot.say("The multiplier has been set to: " + str(payoutM))
        await self.bot.say("In what month does the event happen? (Give as a number)")
        month = await self.bot.wait_for_message(timeout = 30, author = user)
        if month is None:
            await self.bot.say("You didn't enter anything. Event cancelled")
            return
        try:
            month = int(month.contents)
        except ValueError:
            await self.bot.say("You have to enter a number. Event cancelled")
            return
        await self.bot.say("What day of the month does the event happen? (Must be a number)")
        day = await self.bot.wait_for_message(timeout=30, author = user)
        if day is None:
            await self.bot.say("You didn't enter anything. Event cancelled")
            return
        try:
            day = int(day.content)
        except ValueError:
            await self.bot.say("You have to enter a number. Event cancelled")
            return 
        await self.bot.say("What hour of the day does the event happen? (Must be in 24 hour format IE: 9PM is 21)")
        hour = await self.bot.wait_for_message(timeout=30, author = user)
        if hour is None:
            await self.bot.say("You didn't enter anything. Event cancelled")
            return
        try:
            hour = int(hour.content)
        except ValueError:
            await self.bot.say("You have to enter a number. Event cancelled")
            return
        await self.bot.say("The event happens at " + str(hour) + ":00 on " + str(month) + "/" + str(day))
        
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
