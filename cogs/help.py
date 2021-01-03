import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, kita):
        self.kita = kita

    def cmd_list(self):
        cmdlist = []
        for cmd in self.kita.commands:
            if cmd.hidden == False:
                cmdlist.append(cmd.name)
        
        cmdlist = ', '.join(cmdlist)
        return cmdlist

    @commands.command(name='help', help='Everyone needs a bit of help', hidden=True)
    async def help(self, ctx, cmd = None):
        if cmd == None:
            embed = discord.Embed(title='Kita Help', description='**[:desktop: Github](https://github.com/MarkussGitHub/Kita)** **[:envelope: Invite](https://discord.com/api/oauth2/authorize?client_id=792091990387982366&permissions=8&scope=bot)**')
            embed.add_field(name='Commands', value=f'```{self.cmd_list()}```')
            embed.set_footer(text='ki help <command name> to see info on specific command')
            await ctx.send(embed=embed)
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
