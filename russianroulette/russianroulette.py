import discord
from discord.ext import commands
import os
from .utils.dataIO import dataIO
import time
import asyncio

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
                await self.betAmount()
            else:
                await self.bot.say("Start")
        elif type.lower() == "join":
            await self.bot.say("Join")
        else:
            await self.bot.say(user.mention + " This command only accepts 'start' or 'join'")
            
    async def betAmount():
        await self.bot.say("How much would you like to put on the line: $")
        bet = await self.bot.wait_for_message(timeout=60, author=user, check=check)
        if bet is int:
            bet = int(float(bet))
            await self.bot.say("Bet placed at $" + string(bet))
        else:
            await self.bot.say("You must enter a number")
            await self.betAmount()
            

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
