import discord
from discord.ext import commands
import keep_alive, os
kita = commands.Bot("kita ", case_insensitive=True, intents=discord.Intents.all())

@kita.event
async def on_ready():
  print('Kita is ready!')

keep_alive.keep_alive()
kita.run(os.getenv("TOKEN"))
