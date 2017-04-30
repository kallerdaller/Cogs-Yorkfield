import discord
from discord.ext import commands
import os
from .utils.dataIO import dataIO
import time
import asyncio

client = discord.Client()

class Russianroulette:
    """Russian Roulette"""
    
    def __init__(self, bot):
        self.bot = bot
        self.file_path = "data/russianroulette/russianroulette.json"
        self.json_data = dataIO.load_json(self.file_path) 
    

        
    @commands.command(pass_context=True, aliases=["rr", "russian"])
    async def russianroulette(self, ctx, type):
        """Type = start or join"""
        
        #Your code will go here
        user = ctx.message.author
        bank = self.bot.get_cog("Economy").bank
        if type.lower() == "start":
            if self.json_data["System"]["Status"] == "Stopped":
                await self.bot.say("Bet")
                await self.betAmount(user)
            else:
                await self.bot.say("Start")
        elif type.lower() == "join":
            await self.bot.say("Join")
        else:
            await self.bot.say(user.mention + " This command only accepts 'start' or 'join'")
            
    @client.event
    async def betAmount(self, user):
        await self.bot.say("How much would you like to put on the line: $")
        bet = await self.bot.wait_for_message(timeout=30, author=user)
        if bet is None:
            await self.bot.say("You didn't enter anything")
            return
        bet = int(str(bet.content))
        print(type(bet))
        typeas = type(bet)
        print(typeas)
        if isinstance(bet , class 'int'):
            await self.bot.say("Bet placed at $" + string(bet))
        else:
            await self.bot.say("You must enter a number")
            await self.betAmount(user)
            

def check_folders():
    if not os.path.exists("data/russianroulette"): 
        print("Creating data/russianroulette floder...")  
        os.makedirs("data/russianroulette") 

def check_files(): 
    system = {"System": {"Pot": 0,            
                         "Active": False,
                         "Bet": 0,
                         "Roulette Initial": False,
                         "Status": "Stopped",
                         "Player Count": 0},
              "Players": {},
              "Config": {"Min Bet": 10}}

    f = "data/russianroulette/russianroulette.json"
    if not dataIO.is_valid_json(f):
        print("Creating defualt russianroulette.json...")
        dataIO.save_json(f, system)

def setup(bot):
    check_folders()
    check_files()
    n = Russianroulette(bot)
    bot.add_cog(n)
