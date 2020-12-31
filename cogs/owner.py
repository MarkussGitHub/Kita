import discord
from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, kita):
        self.kita = kita
  
    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, *, cog):
        """Reload cog"""
        try:
            self.kita.unload_extension(cog)
            self.kita.load_extension(cog)
        except Exception as e:
            embed = discord.Embed(title='RELOAD FAILED!', description=f'**`ERROR:`** {e}', color=0xFF0000)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='RELOAD SUCCESFFUL!', description=f'**``{cog}``** has been reloaded!', color=0x90ee90)
            await ctx.send(embed=embed)
    
    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def _load(self, ctx, *, cog):
        """Load cog"""
        try:
            self.kita.load_extension(cog)
        except Exception as e:
            embed = discord.Embed(title='LOAD FAILED!', description=f'**`ERROR:`** {e}', color=0xFF0000)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='LOAD SUCCESSFUL!', description=f'**``{cog}``** has been loaded!', color=0x90ee90)
            await ctx.send(embed=embed)
    
def setup(kita):
    kita.add_cog(Owner(kita))
