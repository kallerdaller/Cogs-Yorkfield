import discord
from discord.ext import commands
from discord.permissions import Permissions
from .utils import checks
import asyncio
from .utils.dataIO import dataIO
import os
import datetime

client = discord.Client()

class EventBets:
    """Create an event which people can bet on"""

    def __init__(self, bot):
        self.bot = bot
        self.file_path = "data/irlbetting/irlbetting.json"
        self.json_data = dataIO.load_json(self.file_path) 

    @commands.command(pass_context=True, aliases=["ce", "eventcreate"])
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
            await self.bot.say("You need atleast 2 outcomes. Event cancelled")
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
            month = int(month.content)
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
        numberofcurrentevents = self.json_data["Events"]["CurrentEvents"]
        self.json_data["Events"][str(numberofcurrentevents+1)] = {}
        self.json_data["Events"][str(numberofcurrentevents+1)]["Name"] = eventname
        self.json_data["Events"][str(numberofcurrentevents+1)]["Multiplier"] = payoutM
        self.json_data["Events"][str(numberofcurrentevents+1)]["Date"] = {}
        self.json_data["Events"][str(numberofcurrentevents+1)]["Date"]["Month"] = month
        self.json_data["Events"][str(numberofcurrentevents+1)]["Date"]["Day"] = day
        self.json_data["Events"][str(numberofcurrentevents+1)]["Date"]["Hour"] = hour
        self.json_data["Events"][str(numberofcurrentevents+1)]["Users"] = {}
        self.json_data["Events"][str(numberofcurrentevents+1)]["CurrentUsers"] = 0
        self.json_data["Events"][str(numberofcurrentevents+1)]["Outcomes"] = {}
        c = 0
        while c < len(outcome)-1:
            self.json_data["Events"][str(numberofcurrentevents+1)]["Outcomes"][str(c+1)] = outcome[c]
            c += 1
        self.json_data["Events"]["CurrentEvents"] = self.json_data["Events"]["CurrentEvents"]+1
        dataIO.save_json(self.file_path, self.json_data)
        
        
    @commands.command(pass_context=True, aliases=["be", "eventbet"])
    @client.event
    async def betevent(self, ctx):
        """Bet on event"""
        
        user = ctx.message.author
        bank = self.bot.get_cog('Economy').bank
        if not bank.account_exists(user):
            await self.bot.say("You don't have a bank account so you can't bet on events. Do `*bank register` to make an account")
            return
        numberofcurrentevents = self.json_data["Events"]["CurrentEvents"]
        a = 1
        if numberofcurrentevents == 0:
            await self.bot.say("There are no events running right now, sorry")
            return
        await self.bot.say("Which event would you like to bet on?: ")
        while a <= numberofcurrentevents:
            await self.bot.say(str(a) + ": " + self.json_data["Events"][str(a)]["Name"])
            a += 1
        await self.bot.say("Enter the number of the event")
        event = await self.bot.wait_for_message(timeout = 30, author = user)
        if event is None:
            await self.bot.say("You didn't enter anything. Bet cancelled")
            return
        try:
            event = int(event.content)
        except ValueError:
            await self.bot.say("You need to enter a number. Bet cancelled")
            return
        if event > numberofcurrentevents:
            await self.bot.say("That is not a valid event number. Bet cancelled")
            return
        i = 1
        while i <= self.json_data["Events"][str(event)]["CurrentUsers"]:
            print(i)
            if user == discord.utils.get(ctx.message.server.members, id=self.json_data["Events"][str(event)]["Users"][str(i)]["ID"]):
                await self.bot.say("You cannot bet on an event more than once. Bet cancelled")
                return
            i += 1
        await self.bot.say("You have picked: " + self.json_data["Events"][str(event)]["Name"] + ". \nThe outcomes for this event are:")
        d = 1
        while d <= len(self.json_data["Events"][str(event)]["Outcomes"]):
            await self.bot.say(str(d) + ": " + self.json_data["Events"][str(event)]["Outcomes"][str(d)])
            d += 1
        await self.bot.say("Enter the number of the outcome you would like to bet on: ")
        outcome = await self.bot.wait_for_message(timeout = 30, author = user)
        if outcome is None:
            await self.bot.say("You didn't enter anything. Bet cancelled")
            return
        try:
            outcome = int(outcome.content)
        except ValueError:
            await self.bot.say("You need to enter a number. Bet cancelled")
            return
        await self.bot.say("You have picked: " + self.json_data["Events"][str(event)]["Outcomes"][str(outcome)] + ". You have $" + str(bank.get_balance(user)) + ". How much would you like to bet?")
        bet = await self.bot.wait_for_message(timeout = 30, author = user)
        if bet is None:
            await self.bot.say("You didn't enter anything. Bet cancelled")
            return
        try:
            bet = int(bet.content)
        except ValueError:
            await self.bot.say("You need to enter a number. Bet cancelled")
            return
        if bet > bank.get_balance(user):
            await self.bot.say("You don't have enough money. Bet cancelled")
            return
        bank.withdraw_credits(user, bet)
        numberofcurrentusers = self.json_data["Events"][str(event)]["CurrentUsers"]
        self.json_data["Events"][str(event)]["Users"][str(numberofcurrentusers+1)] = {}
        self.json_data["Events"][str(event)]["Users"][str(numberofcurrentusers+1)]["ID"] = str(user.id)
        self.json_data["Events"][str(event)]["Users"][str(numberofcurrentusers+1)]["Bet"] = bet
        self.json_data["Events"][str(event)]["Users"][str(numberofcurrentusers+1)]["Choice"] = outcome
        self.json_data["Events"][str(event)]["CurrentUsers"] = self.json_data["Events"][str(event)]["CurrentUsers"]+1
        dataIO.save_json(self.file_path, self.json_data)
        await self.bot.say("You have placed $" + str(bet) + " on " + str(self.json_data["Events"][str(event)]["Users"][str(numberofcurrentusers+1)]["Choice"]))
        
    @commands.command(pass_context=True, aliases=["fe", "finishresults"])
    @checks.admin_or_permissions(manage_server=True)
    @client.event
    async def finishevent(self, ctx):
        """Finish event"""
        
        now = datetime.datetime.now()
        month = now.month
        day = now.day
        hour = now.hour
        await self.bot.say(str(now))
        await self.bot.say(str(now.month))
        await self.bot.say(str(now.day))
        await self.bot.say(str(now.hour))
        await self.bot.say(str(strdatetime.tzinfo))
    
                   
def check_folders():
    if not os.path.exists("data/irlbetting"): 
        print("Creating data/irlbetting floder...")  
        os.makedirs("data/irlbetting") 

        
def check_files(): 
    system = {"Events": {"1": {"Name": "",
                               "CurrentUsers": 0,
                               "Multiplier": 1,
                               "Users": { "1": {"Bet": 0,
                                                "ID": "",
                                                "Choice": ""},
                                        },
                               "Date": {"Hour": 0,
                                        "Day": 0,
                                        "Month": 0},
                               "Outcomes": {"1": ""}},
                        "CurrentEvents": 0}}
                         
    f = "data/irlbetting/irlbetting.json"
    if not dataIO.is_valid_json(f):
        print("Creating defualt irlbetting.json...")
        dataIO.save_json(f, system)
        
        
def setup(bot):
    check_folders()
    check_files()
    n = EventBets(bot)
    bot.add_cog(n)
