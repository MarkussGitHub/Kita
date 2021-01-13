import discord
from discord.ext import commands, tasks

class Help(commands.Cog):
    def __init__(self, kita):
        self.kita = kita

    def cmd_list(self, cog):
        cmdlist = []
        for cmd in self.kita.commands:
            if cmd.cog_name == cog:
                if cmd.hidden == False:
                    cmdlist.append(cmd.name)
        
        cmdlist = ', '.join(cmdlist)
        return cmdlist

    def ctgry_list(self):
        ctgrylist = []
        forbidden = ['Owner', 'Info', 'Dev', 'Help']
        for ctgry in self.kita.cogs:
            if ctgry not in forbidden:
                ctgrylist.append(ctgry)

        ctgrylist = ', '.join(ctgrylist)
        return ctgrylist

    @tasks.loop(seconds=1)
    async def paginator(self, helpmsg, page1, page2, author):
        def check(reaction, user):
            return user == author and reaction.message.id == helpmsg.id
        reaction, user = await self.kita.wait_for('reaction_add', check=check)
        if reaction.emoji == '⏩':
            await reaction.remove(author)
            await helpmsg.edit(embed=page2)
        elif reaction.emoji == '⏪':
            await reaction.remove(author)
            await helpmsg.edit(embed=page1)

    @commands.command(name='help', help='Everyone needs a bit of help', hidden=True)
    async def help(self, ctx, cmd = None):
        self.paginator.cancel()
        if cmd == None:
            page1 = discord.Embed(title='Kita Help', description='**[:desktop: Github](https://github.com/MarkussGitHub/Kita)** **[:envelope: Invite](https://discord.com/api/oauth2/authorize?client_id=792091990387982366&permissions=8&scope=bot)**', color=0xF2F2F2)
            page1.add_field(name='Categories', value=f'```{self.ctgry_list()}```')
            page1.set_footer(text='ki help <command name> to see info on specific command')
            page2 = discord.Embed(title='Kita commands', color=0xF2F2F2)
            page2.add_field(name='Fun', value=f'```{self.cmd_list("Fun")}```', inline=False)
            page2.add_field(name='Games', value=f'```{self.cmd_list("Games")}```', inline=False)
            page2.add_field(name='Mod', value=f'```{self.cmd_list("Mod")}```', inline=False)
            page2.set_footer(text='ki help <command name> to see info on specific command')
            helpmsg = await ctx.send(embed=page1)
            await helpmsg.add_reaction('⏪')
            await helpmsg.add_reaction('⏩')
            self.paginator.start(helpmsg, page1, page2, ctx.author)
        else:
            for command in self.kita.commands:
                if command.name == cmd:
                    for key, value in command.clean_params.items(): 
                        arg = key
                        break
                    else:
                        arg = None
                    embed = discord.Embed(title=f'{cmd.capitalize()} Help', description=command.help)
                    if arg != None:
                        embed.add_field(name='Usage', value=f'```ki {cmd} <{arg}>```')
                    else:
                        embed.add_field(name='Usage', value=f'```ki {cmd}```')

                    if len(command.aliases) > 0:
                        aliaslist = ', '.join(command.aliases)
                    else:
                        aliaslist = None

                    embed.add_field(name='Aliases', value=f'```{aliaslist}```', inline=False)
                    await ctx.send(embed=embed)
                    break
            else:
                embed = discord.Embed(description='There is no such command', color=0xFF0000)
                await ctx.send(embed=embed)

def setup(kita):
    kita.add_cog(Help(kita))
