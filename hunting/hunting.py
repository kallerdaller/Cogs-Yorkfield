import discord
from discord.ext import commands
from .utils import checks
import asyncio
from .utils.dataIO import dataIO
import os
import time

client = discord.Client()

class Hunting:
    """Shoot the pesky animals"""
    
    def __init__(self, bot):
        self.bot = bot
        self.file_path = "data/hunting/hunting.json"
        self.json_data = dataIO.load_json(self.file_path) 
