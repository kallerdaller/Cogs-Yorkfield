from pylab import scatter, plot, grid, show, savefig
from matplotlib import pyplot as plt
from discord.ext import commands
from __main__ import send_cmd_help
from cogs.utils import checks
from cogs.utils.dataIO import dataIO
from os import path, makedirs

class SimpleGraph:

    def __init__(self, bot):
        self.bot = bot
        self.settings = dataIO.load_json('data/sgraph/settings.json')
        self.normalposition = {'x':0, 'y':0}
        self.position = self.normalposition

    @commands.group(aliases=['graph','sgraph'], pass_context=True)
    @checks.admin()
    async def simplegraph(self, ctx):
        """2d graph creator in discord"""
        if ctx.invoked_subcommand is None:
            await self.bot.send_cmd_help(ctx)

    @simplegraph.command(name='reset')
    async def _reset(self):
        """Reset all values"""

        self.position = self.normalposition
        self.size = self.normalsize

        await self.bot.say('Reset values')

    @simplegraph.command(name='set', pass_context=True)
    async def _set_position(self, ctx, x:int=None, y:int=None):
        """Set Coordinates"""

        if x == None and y == None:
            await send_cmd_help(ctx)
            await self.bot.say('```Current Position\nX:{}\nY:{}```'.format(self.position['x'], self.position['y']))
            return

        if x != None:
            self.position['x'] = x

        if y != None:
            self.position['y'] = y

        await self.bot.say('Set coordinates to\n```X:{}\nY:{}```'.format(self.position['x'], self.position['y']))

    @simplegraph.command(name='graph')
    async def _show(self):
        """Print out a graph"""

        if self.position == {'x':0, 'y':0}:
            await self.bot.say('```Move the line first using [p]move```')
            return

        message = await self.bot.say('Uploading graph...')

        x = [self.position['x']]
        y = [self.position['y']]
        color=['m','g','r','b']

        fig = plt.figure()
        ax = fig.add_subplot(111)

        scatter(x,y, s=100 ,marker='o', c=color)

        [ plot( [dot_x,dot_x] ,[0,dot_y], '-', linewidth = 3 ) for dot_x,dot_y in zip(x,y) ]
        [ plot( [0,dot_x] ,[dot_y,dot_y], '-', linewidth = 3 ) for dot_x,dot_y in zip(x,y) ]

        left,right = ax.get_xlim()
        low,high = ax.get_ylim()

        grid()

        filename = 'graph.png'
        filepath = 'data/sgraph/temp/' + filename

        with open(filepath, 'wb') as f:
            savefig(f)

        await self.bot.delete_message(message)
        await self.bot.upload(filepath)

def check_folder():  # Paddo is great
    print("BLEH")
    if not path.exists("data/sgraph"):
        print("[SimpleGraph]Creating data/sgraph folder...")
        makedirs("data/sgraph")
        dataIO.save_json("data/sgraph/settings.json", {})

    if not path.exists("data/sgraph/temp"):
        print("[SimpleGraph]Creating data/sgraph/temp folder...")
        makedirs("data/sgraph/temp")



def setup(bot):
    check_folder()
    bot.add_cog(SimpleGraph(bot))
