import discord
from discord.ext import commands
import os
from .utils.dataIO import dataIO
import time
import asyncio
from random import randint

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
                if user.id == self.json_data["Players"]["1"] and self.json_data["System"]["Player Count"] > 1:
                    totalPlayers = self.json_data["System"]["Player Count"]
                    await self.startGame(bank, ctx, totalPlayers)
                else:
                    await self.bot.say("Game has been made, to join it type `*rr join`. Only the creator of the roulette can start it and there must be more than 1 person")
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
                await self.bot.say("The game is running and can only be stopped when waiting in the lobby")
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
                await self.bot.say("The roulette has been cancelled")
            else:
                await self.bot.say("You must be the person who started the roulette and you must currently be waiting for people to join")
        else:
            await self.bot.say(user.mention + "This command only accepts `start` `stop` or `join`")
            
    @client.event
    async def betAmount(self, user, bank):
        await self.bot.say("How much would you like to put on the line: $")
        bet = await self.bot.wait_for_message(timeout=10, author=user)
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
                await self.bot.say("You don't have a bank account, create one first with `*bank register`")
                return               
        else:
            await self.bot.say("You must enter a number")
            await self.betAmount(user, bank)
    
    async def joinGame(self, user, bank):
        bet = self.json_data["System"]["Bet"]
        if self.json_data["System"]["Player Count"] == 6:
            await self.bot.say("The game is full, please wait until it has finished to join")
        elif bank.account_exists(user):
            if user.id == self.json_data["Players"]["1"] or user.id == self.json_data["Players"]["2"] or user.id == self.json_data["Players"]["3"] or user.id == self.json_data["Players"]["4"] or user.id == self.json_data["Players"]["5"] or user.id == self.json_data["Players"]["6"]:
                await self.bot.say("You're already entered")
            else:
                if bank.get_balance(user) > bet:
                    await self.bot.say("The bet is set to: $" + str(bet) + "\nWould you still like to enter? Y/N")
                    answer = ""
                    answer = await self.bot.wait_for_message(timeout=10, author=user)
                    answer = str(answer.content)
                    if answer is None or answer.lower() == "n" or answer.lower() == "no":
                        await self.bot.say("Very well, you haven't been entered")
                        return
                    elif answer.lower() == "y" or answer.lower() == "yes":
                        self.json_data["System"]["Player Count"] += 1
                        self.json_data["Players"][str(self.json_data["System"]["Player Count"])] = user.id
                        f = "data/russianroulette/russianroulette.json"
                        dataIO.save_json(f, self.json_data)
                        await self.bot.say("You have been entered. You are in seat: " + str(self.json_data["System"]["Player Count"]))
                        return
                else:
                    await self.bot.say("You don't have enough money. You have $" + str(bank.get_balance(user)) + " The bet is set at $" + str(bet))
                    return
        else:
            await self.bot.say("You don't have a bank account. Make one with `*bank register`")
            return
        
    async def startGame(self, bank, ctx, totalPlayers):
        i = 1
        a = 1
        await self.bot.say("Game is starting")
        while i <= self.json_data["System"]["Player Count"]:
            bank.withdraw_credits(discord.utils.get(ctx.message.server.members, id=self.json_data["Players"][str(i)]), self.json_data["System"]["Bet"])
            i += 1
        while self.json_data["System"]["Player Count"] > 1:
            await self.play(ctx, a)
            a += 1
        b = 1
        winner = ""
        while winner == "":
            if self.json_data["Players"][str(b)] == "":
                b += 1
            else:
                winner = self.json_data["Players"][str(b)]
        bank.deposit_credits(discord.utils.get(ctx.message.server.members, id=winner), self.json_data["System"]["Bet"] * totalPlayers)
        await self.bot.say("Congrats " + discord.utils.get(ctx.message.server.members, id=winner).mention + " on winning $" + str(self.json_data["System"]["Bet"] * totalPlayers))
            
        
    async def play(self, ctx, a):
        try:
            if self.json_data["Players"][str((a%7))] == "":
                return
        except KeyError:
            return
        time.sleep(2)
        await self.bot.say(discord.utils.get(ctx.message.server.members, id=self.json_data["Players"][str(a%7)]).mention + " picks up the gun...")
        time.sleep(2)
        await self.bot.say("They pull the trigger...")
        time.sleep(1)
        if randint(1, 20) >= 9:
            await self.bot.say(discord.utils.get(ctx.message.server.members, id=self.json_data["Players"][str((a%7))]).mention + " you're still alive")
        else: 
            await self.bot.say(discord.utils.get(ctx.message.server.members, id=self.json_data["Players"][str((a%7))]).mention + " shot their brains out")
            self.json_data["Players"][str((a%6))] = ""
            self.json_data["System"]["Player Count"] += -1
            f = "data/russianroulette/russianroulette.json"
            dataIO.save_json(f, self.json_data)
            

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
