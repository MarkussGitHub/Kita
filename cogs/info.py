import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, kita):
        self.kita = kita

    @commands.command(name='info', help='Bot info')
    async def info(self, ctx):
        embed = discord.Embed(title='Kita Info', color=0xF2F2F2)
        embed.add_field(name='Running on', value=f'``Discord.py {discord.__version__}``')
        embed.add_field(name='Servers', value=f'``{len(self.kita.guilds)} servers``')
        embed.add_field(name='Users', value=f'``{len(set(self.kita.get_all_members()))} users``')
        await ctx.send(embed=embed)
        
def setup(kita):
    kita.add_cog(Info(kita))
