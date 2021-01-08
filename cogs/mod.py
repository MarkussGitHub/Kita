import discord
from discord.ext import commands

class Mod(commands.Cog):
    def __init__(self, kita):
        self.kita = kita

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason: str = 'None'):
        if ctx.author.guild_permissions > member.guild_permissions < ctx.guild.me.guild_permissions:
            embed = discord.Embed(title='Kick successful!', 
                                  description=f'{ctx.author.mention} kicked **{member.display_name}**!',
                                  color=0xF2F2F2)
            embed.add_field(name='Reason', value=f'``{reason}``')
            await ctx.guild.kick(user=member, reason=reason)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='Kick unsuccessful!', 
                                  description=f'Couldnt kick **{member.display_name}**',
                                  color=0xFF0000)
            embed.add_field(name='Reason', value=f'``Specified user, has more power than you or me!``')
            await ctx.send(embed=embed)


    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Member not specified!',
                                  description='You didnt specify member to kick!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='Missing permissions!',
                                  description='You dont have permissions to kick people!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(title='Bot is missing permissions!',
                                  description='Bot doesnt have permissions to kick people!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(title='Member not found!',
                                  description='Couldnt find member that you specified!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)


def setup(kita):
    kita.add_cog(Mod(kita))
