import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, kita):
        self.kita = kita

    @commands.group(name='help', invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title='Kita Help', description='**[:desktop: Github](https://github.com/MarkussGitHub/Kita)** **[:envelope: Invite](https://discord.com/api/oauth2/authorize?client_id=792091990387982366&permissions=8&scope=bot)**')
        embed.add_field(name='Commands', 
                        value='```avatar, explain, flip, meme, roll, spotify, help```')
        await ctx.send(embed=embed)

def setup(kita):
    kita.add_cog(Help(kita))
