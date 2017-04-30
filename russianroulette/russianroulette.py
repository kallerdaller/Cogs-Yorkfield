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
                await self.betAmount(user, bank)
            elif self.json_data["System"]["Status"] == "Waiting":
                await self.bot.say("Game has been made, to join it type `*rr join`")
            else:
                await self.bot.say("Game is in progress, please wait until it's finished")
        elif type.lower() == "join":
            if self.json_data["System"]["Status"] == "Waiting":
                await self.joinGame(user, bank)
            elif self.json_data["System"]["Status"] == "Stopped":
                await self.bot.say("No game to join, type `*rr start` to create a game")
            else:
                await self.bot.say("Game is in progress, please wait until it's finished")
        elif type.lower() == "stop":
            if self.json_data["System"]["Status"] == "Stopped":
                await self.bot.say("There is no game running to stop")
            elif self.json_data["System"]["Status"] == "Running":
                await self.bot.say("The game is running and can only be stopped when in the lobby waiting")
            if user.id == self.json_data["Players"]["1"]:
                self.json_data["Players"]["1"] = ""
                self.json_data["Players"]["2"] = ""
                self.json_data["Players"]["3"] = ""
                self.json_data["Players"]["4"] = ""
                self.json_data["Players"]["5"] = ""
                self.json_data["Players"]["6"] = ""
                self.json_data["System"]["Player Count"] = 0
                self.json_data["System"]["Status"] = "Stopped"
                self.json_data["System"]["Bet"] = 0
                f = "data/russianroulette/russianroulette.json"
                dataIO.save_json(f, self.json_data)
            else:
                await self.bot.say("You must be the person who started the roulette and you must currently be waiting for people to join")
        else:
            await self.bot.say(user.mention + "`This command only accepts `start` `stop` or `join`")
            
    @client.event
    async def betAmount(self, user, bank):
        await self.bot.say("How much would you like to put on the line: $")
        bet = await self.bot.wait_for_message(timeout=30, author=user)
        if bet is None:
            await self.bot.say("You didn't enter anything")
            return
        try:
            bet = int(str(bet.content))
        except ValueError:
            pass
        if isinstance(bet , int):
            if bank.account_exists(user):
                if bank.get_balance(user) > bet:
                    self.json_data["System"]["Bet"] = bet
                    self.json_data["Players"]["1"] = user.id
                    self.json_data["System"]["Player Count"] += 1
                    self.json_data["System"]["Status"] = "Waiting"
                    f = "data/russianroulette/russianroulette.json"
                    dataIO.save_json(f, self.json_data)
                    await self.bot.say("Bet placed at $" + str(bet) + "\nTo start the game you need atleast one another person to join with `*rr join`")
                else:
                    await self.bot.say("You don't have enough to place a bet of $" + str(bet) + " You only have $" + str(bank.get_balance(user)))
            else:
                await self.bot.say("You don't have a bank account, create one first with *bank register")
                return               
        else:
            await self.bot.say("You must enter a number")
            await self.betAmount(user, bank)
    
    async def joinGame(self, user, bank):
        await self.bot.say("asd")
            

def check_folders():
    if not os.path.exists("data/russianroulette"): 
        print("Creating data/russianroulette floder...")  
        os.makedirs("data/russianroulette") 

def check_files(): 
    system = {"System": {"Bet": 0,
                         "Status": "Stopped",
                         "Player Count": 0},
              "Players": {"1": "",
                          "2": "",
                          "3": "",
                          "4": "",
                          "5": "",
                          "6": ""}}
    f = "data/russianroulette/russianroulette.json"
    if not dataIO.is_valid_json(f):
        print("Creating defualt russianroulette.json...")
        dataIO.save_json(f, system)

def setup(bot):
    check_folders()
    check_files()
    n = Russianroulette(bot)
    bot.add_cog(n)
