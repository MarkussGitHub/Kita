import discord
from discord.ext import commands
from typing import Union

class Dev(commands.Cog):
    def __init__(self, kita):
        self.kita = kita

    class GuildConverter(commands.Converter):
        async def convert(self, ctx, argument):
            bot = ctx.bot
            server = await bot.fetch_guild(argument)
            return server
    
    class OperatorConverter(commands.Converter):
        async def convert(self, ctx, argument):
            Operator = ['+', '-', '*', '/', '%', '=', '>', '<', '!=', '^']
            for instance in Operator:
                if instance in argument:
                    return [argument, 'Operator']
                    break
            else:
                argument: str
                return argument
    
    class EvalConverter(commands.Converter):
        async def convert(self, ctx, argument):
            result = eval(argument)
            return result

    @commands.command(name='type')
    async def type(self, ctx, *, 
                         argument: Union[discord.Member, discord.User, GuildConverter,
                                        discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel,
                                        discord.Role, discord.Message, discord.Emoji,
                                        int, bool, float, complex, EvalConverter, OperatorConverter, str]):
        embed = discord.Embed(title='Type of input')
        if type(argument).__name__ != "list":
            embed.add_field(name='Input:', value=f'```{argument}```', inline=False)
            embed.add_field(name='Output:', value=f'```{type(argument).__name__}```')
        else:
            embed.add_field(name='Input:', value=f'```{argument[0]}```', inline=False)
            embed.add_field(name='Output:', value=f'```{argument[1]}```')
        embed.set_footer(text='Beta version')
        
        await ctx.send(embed=embed)

    @type.error
    async def type_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Missing Argument', description='You didnt give me anything to determine type of', color=0xFF0000)
            embed.add_field(name='Example usage', value='```ki type lmao```', inline=False)
            await ctx.send(embed=embed)

def setup(kita):
    kita.add_cog(Dev(kita))
