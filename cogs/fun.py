import discord
import requests, io
import asyncio
from discord import Spotify
from discord.ext import commands
from datetime import datetime
from random import randint, randrange, choice
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

def hexgen():
    color = randint(0, 0xFFFFFF)
    return color

class Fun(commands.Cog):
    def __init__(self, kita):
        self.kita = kita

    @commands.command(name='poll', help='Make a poll')
    async def poll(self, ctx, *, question: str):
        embed = discord.Embed(title='Poll', description=f'{question}', color=hexgen())
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')
        await asyncio.sleep(10)
        message = await ctx.channel.fetch_message(msg.id)
        for react in message.reactions:
            if react.emoji == '✅':
                yes = react.count
            if react.emoji == '❌':
                no = react.count
        await msg.delete()
        embed = discord.Embed(title='Poll results', 
                              description=f'✅ had {yes} votes\n\n'
                                          f'❌ had {no} votes',
                              color=hexgen())
        await ctx.send(embed=embed)

        
    @commands.command(name='explain', help='Have a word with unknown meaning?')
    async def explain(self, ctx, term):
        url = f'http://api.urbandictionary.com/v0/define?term={term}'
        r = requests.get(url).json()

        correct = 0
        for idx, value in enumerate(r['list']):
            if value['thumbs_up'] > correct:
                correct = value['thumbs_up']
                correctIndex = idx
        
        author = r['list'][correctIndex]['author']
        definition = r['list'][correctIndex]['definition']
        url = r['list'][correctIndex]['permalink']
        writtenOn = r['list'][correctIndex]['written_on'].split("T")[0]

        embed = discord.Embed(title=f'{term}', url=url,
                            description=f'```{definition}```', color=hexgen())
        embed.set_footer(text=f'Defined by {author}, {writtenOn}')
        await ctx.send(embed=embed)

    @explain.error
    async def explain_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title='Missing Argument', description='You didnt tell me which word to explain!', color=0xFF0000)
            embed.add_field(name='Example usage', value='```ki explain lmao```', inline=False)
            embed.add_field(name='Expected response', value='```[Laughing] [My Ass Off]. Used [online] only.```')
            await ctx.send(embed=embed)

    @commands.command(name='spotify', aliases=['sp'], help='Flex with your music, or check out what others listen to')
    async def spotify(self, ctx, *, user: discord.Member = None):
        sp = None
        if user == None:
            user = ctx.author
        
        if user.activities:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    sp = activity

        if sp == None:
            if user == ctx.author:
                embed = discord.Embed(description='You arent listening to anything', color=0xFF0000)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(description=f'{user.display_name} isnt listening to anything', color=0xFF0000)
                await ctx.send(embed=embed)
        else:
            spotify = Image.new('RGBA', (500, 220), 'white')
            line = Image.open('src/line.png')
            songFont = ImageFont.truetype('fonts/arialUnicode.ttf', 24, encoding="unic")
            artistFont = ImageFont.truetype('fonts/arialUnicode.ttf', 16, encoding="unic")
            timeFont = ImageFont.truetype("fonts/arialUnicode.ttf", 12, encoding="unic")

            r = requests.get(sp.album_cover_url)
            bg = Image.open(io.BytesIO(r.content)).filter(ImageFilter.GaussianBlur(radius=6))
            enhancer = ImageEnhance.Brightness(bg)
            newBG = enhancer.enhance(0.55)
            album_cover = Image.open(io.BytesIO(r.content)).resize((100 ,100))
            spotify.paste(newBG, (-80, -150))
            spotify.paste(album_cover, (200, 20))

            if len(sp.title) >= 25:
                dots = "." * 3
                title = sp.title[0:25] + dots
            else:
                title = sp.title

            if len(sp.artist) >= 25:
                dots = "." * 3
                artist = sp.artist[0:25] + dots
            else:
                artist = sp.artist

            draw = ImageDraw.Draw(spotify)
            w, h = draw.textsize(title, font=songFont)
            draw.text(((500-w)/2, 130), u"{}".format(title), font=songFont, fill='white')

            artist = sp.artist
            w, h = draw.textsize(artist, font=artistFont)
            draw.text(((500-w)/2, 160), u"{}".format(artist), font=artistFont, fill='white')

            ongoing = sp.end - datetime.utcnow()
            ongoing = str((sp.duration - ongoing).total_seconds()).split(".")[0]
            ongoingMinutes = int(ongoing) // 60
            ongoingSeconds = int(ongoing) % 60
            ongoingSeconds = f'{ongoingSeconds:02d}'
            ongoing = f'{ongoingMinutes}:{ongoingSeconds}'
            draw.text((90, 190), ongoing, font=timeFont, fill='white')

            duration = str(sp.duration.total_seconds()).split(".")[0]
            maxMinutes = int(duration) // 60
            maxSeconds = int(duration) % 60
            maxSeconds = f"{maxSeconds:02d}"
            duration = f'{maxMinutes}:{maxSeconds}'
            draw.text((385, 190), duration, font=timeFont, fill='white')

            spotify.paste(line, (0, 175), line)

            buffer = io.BytesIO()
            spotify.save(buffer, format='PNG')
            buffer.seek(0)
            file = discord.File(buffer, 'spotify.png')
            embed = discord.Embed(description=f'[Listen on spotify](https://open.spotify.com/track/{sp.track_id})', color=0xF2F2F2)
            embed.set_image(url='attachment://spotify.png')
            await ctx.send(embed=embed, file=file)

    @commands.command(name='avatar', help='Get your or someones avatar.')
    async def avatar(self, ctx, *, user: discord.User = None):
        if user == None:
            r = requests.get(ctx.author.avatar_url)
        else:
            r = requests.get(user.avatar_url)
        avatar = Image.open(io.BytesIO(r.content))
        buffer = io.BytesIO()
        avatar.save(buffer, format='PNG')
        buffer.seek(0)
        file = discord.File(buffer, "avatar.png")
        await ctx.send(file=file)

    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            embed = discord.Embed(title='Couldnt find that member', color=0xFF0000)
            await ctx.send(embed=embed)

    @commands.command(name='meme', help='Generate meme',)
    async def meme(self, ctx: commands.Context):
        image = requests.get('https://meme-api.herokuapp.com/gimme').json()
        embed = discord.Embed(color=hexgen())
        embed.set_image(url=image['url'])
        await ctx.send(embed=embed)

    @commands.command(name='roll', help='Rolls a number 0-100')
    async def roll(self, ctx):
        roll = randrange(100)
        embed = discord.Embed(title=f'{ctx.author.display_name} rolled **``{roll}``**', color=hexgen())
        await ctx.send(embed=embed)

    @commands.command(name='flip', help='Flips a coin')
    async def flip(self, ctx):
        coins = ['HEADS',
                'TAILS']
        embed = discord.Embed(title=f'{ctx.author.display_name} got {choice(coins)}', color=hexgen())
        await ctx.send(embed=embed)

def setup(kita):
    kita.add_cog(Fun(kita))
