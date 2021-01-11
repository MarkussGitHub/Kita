import discord
from discord.ext import commands

class Mod(commands.Cog):
    def __init__(self, kita):
        self.kita = kita

    class BannedUser(commands.Converter):
        async def convert(self, ctx, id: int):
            bot = ctx.bot
            try:
                user = await bot.fetch_user(id)
            except discord.errors.HTTPException:
                return None
            else:
                return user

    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def unban(self, ctx, id: BannedUser, reason: str = 'None'):
        if id != None:
            embed = discord.Embed(title='Ban remove successful!', 
                                    description=f'{ctx.author.mention} unbanned **{id.display_name}**!',
                                    color=0xF2F2F2)
            embed.add_field(name='Reason', value=f'``{reason}``')
            await ctx.guild.unban(user=id, reason=reason)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='ID not found!',
                                  description='You gave me incorrect id, or the person isnt banned!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
    
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Member not specified!',
                                  description='You didnt specify member to unban!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='Missing permissions!',
                                  description='You dont have permissions to unban people!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(title='Bot is missing permissions!',
                                  description='Bot doesnt have permissions to unban people!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason: str = 'None'):
        if ctx.author.guild_permissions > member.guild_permissions < ctx.guild.me.guild_permissions:
            embed = discord.Embed(title='Ban successful!', 
                                  description=f'{ctx.author.mention} banned **{member.display_name}**!',
                                  color=0xF2F2F2)
            embed.add_field(name='Reason', value=f'``{reason}``')
            await ctx.guild.ban(user=member, reason=reason)
            await ctx.send(embed=embed)
        elif ctx.author.guild_permissions <= member.guild_permissions:
            embed = discord.Embed(title='Ban unsuccessful!', 
                                  description=f'Couldnt ban **{member.display_name}**',
                                  color=0xFF0000)
            embed.add_field(name='Reason', value=f'``Specified user, has more power than you!``')
            await ctx.send(embed=embed)
        elif ctx.guild.me.guild_permissions <= member.guild_permissions:
            embed = discord.Embed(title='Ban unsuccessful!', 
                                  description=f'Couldnt ban **{member.display_name}**',
                                  color=0xFF0000)
            embed.add_field(name='Reason', value=f'``Specified user, has more power than me!``')


    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Member not specified!',
                                  description='You didnt specify member to ban!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title='Missing permissions!',
                                  description='You dont have permissions to ban people!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(title='Bot is missing permissions!',
                                  description='Bot doesnt have permissions to ban people!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(title='Member not found!',
                                  description='Couldnt find member that you specified!',
                                  color=0xFF0000)
            await ctx.send(embed=embed)

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
        elif ctx.author.guild_permissions <= member.guild_permissions:
            embed = discord.Embed(title='Kick unsuccessful!', 
                                  description=f'Couldnt kick **{member.display_name}**',
                                  color=0xFF0000)
            embed.add_field(name='Reason', value=f'``Specified user, has more power than you!``')
            await ctx.send(embed=embed)
        elif ctx.guild.me.guild_permissions <= member.guild_permissions:
            embed = discord.Embed(title='Kick unsuccessful!', 
                                  description=f'Couldnt kick **{member.display_name}**',
                                  color=0xFF0000)
            embed.add_field(name='Reason', value=f'``Specified user, has more power than me!``')


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
