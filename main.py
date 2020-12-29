import discord
from discord.ext import commands
import keep_alive, os

kita = commands.Bot(
    "ki ",
    description='Kita!',
    case_insensitive=True,
    intents=discord.Intents.all()
)
kita.remove_command('help')

# Loading all of our cogs, from "cogs" folder
for cog in os.listdir('./cogs'):
  if cog.endswith('.py'):
    kita.load_extension(f'cogs.{cog[:-3]}')

@kita.event
async def on_ready():
  print('Kita is ready!')

kita.run(os.getenv("TOKEN"))
