import discord
from discord.ext import commands

class Other(commands.Cog):
    def __init__(self, kita):
        self.kita = kita

    @commands.command(name='info', help='Bot info')
    async def info(self, ctx):
        embed = discord.Embed(title='Kita Info', color=0xF2F2F2)
        embed.add_field(name='Running on', value=f'``Discord.py {discord.__version__}``')
        embed.add_field(name='Servers', value=f'``{len(self.kita.guilds)} servers``')
        embed.add_field(name='Users', value=f'``{len(set(self.kita.get_all_members()))} users``')
        await ctx.send(embed=embed)
    
    @commands.command(name='feedback', help='Leave feedback!', 
                      aliases=['fb', 'suggest', 'suggestion'])
    async def feedback(self, ctx, *, msg: str):
        if len(msg) <= 2048:
            owner = await self.kita.fetch_user(201651700753367040)
            embed = discord.Embed(title='Feedback!', description=msg)
            embed.set_footer(text=f'{ctx.author}, Server: {ctx.guild.name}', icon_url=ctx.author.avatar_url)
            await owner.send(embed=embed)
            response = discord.Embed(title='Success!', 
                                    description='Thank you, for the feedback, it was sent to my owner!')
            await ctx.send(embed=response)
        else: 
            embed = discord.Embed(title='Message is too long!',
                                  description='Your message was too long to send, character limit is **2048**!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
    @feedback.error
    async def feedback_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='No message to send!',
                                  description='You didnt leave any message!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
def setup(kita):
    kita.add_cog(Other(kita))
