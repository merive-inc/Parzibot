import asyncio
import random

import discord
import youtube_dl
from discord import Embed, Colour
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice


class Music(commands.Cog):

    def __init__(self, client):
        """Initialisation client"""
        self.client = client
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
            }
        self.songs, self.current = [], ""

    @cog_ext.cog_slash(name="clearplaylist", description="Clear Music Playlist")
    async def clearplaylist(self, ctx):
        """Clear Music Playlist"""
        if (
            ctx.author.voice is None 
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            embed=Embed(title="**Parzibot** isn't connected to your **Voice Channel**", color=Colour(0xff6868))
            embed.set_thumbnail(url="attachment://ParzibotError.png")
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"), embed=embed)
        elif not self.songs:
            self.songs = []
            discord.utils.get(self.client.voice_clients, guild=ctx.guild).stop()
            embed=Embed(title="**The Playlist** has been cleared", color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        else:
            embed=Embed(title="**The Playlist** is empty", color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)

    @cog_ext.cog_slash(name="join", description="Parzibot Joins to Your Current Voice Channel")
    async def join(self, ctx):
        """Parzibot Joins to Your Current Voice Channel"""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if ctx.author.voice is not None and voice is None or not voice.is_connected():
            channel = ctx.author.voice.channel
            await channel.connect()
            embed=Embed(title="**Parzibot** has been connected to **Voice Channel**", color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        else:
            embed=Embed(title="**Parzibot** already connected to **Voice Channel**", color=Colour(0xff6868))
            embed.set_thumbnail(url="attachment://ParzibotError.png")
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"), embed=embed)

    @cog_ext.cog_slash(name="leave", description="Parzibot Leaves from Your Current Voice Channel")
    async def leave(self, ctx):
        """Parzibot Leaves Your Current Voice Channel"""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if ctx.author.voice is None or (
                ctx.author.voice.channel != ctx.voice_client.channel or voice.is_connected() is None):
                embed=Embed(title="**Parzibot** isn't connected to your **Voice Channel**", color=Colour(0xff6868))
                embed.set_thumbnail(url="attachment://ParzibotError.png")
                await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"), embed=embed)
        else:
            self.songs, self.current = [], ""
            await voice.disconnect()
            embed=Embed(title="**Parzibot** has left **Voice Channel**", color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)

    @cog_ext.cog_slash(
        name="musichelp",
        description="The List of Parzibot Music Commands",
        options=[
            create_option(
                name="command",
                description="The Help Message for Specific Music Command",
                option_type=3,
                required=False,
                choices=[
                    create_choice(name="clearplaylist", value="clearplaylist"),
                    create_choice(name="join", value="join"),
                    create_choice(name="leave", value="leave"),
                    create_choice(name="musichelp", value="musichelp"),
                    create_choice(name="next", value="next"),
                    create_choice(name="pause", value="pause"),
                    create_choice(name="play", value="play"),
                    create_choice(name="playlist", value="playlist"),
                    create_choice(name="replay", value="replay"),
                    create_choice(name="resume", value="resume"),
                    create_choice(name="shuffle", value="shuffle"),                    
                    create_choice(name="stop", value="stop")
                    ])
            ])
    async def musichelp(self, ctx, command=None):
        """The List of Parzibot Music Commands"""
        if command is None:
            embed=Embed(
                title=f"Music commands",
                description=(
                    ' - **/clearplaylist** - Clear Music Playlist\n'
                    ' - **/join** - Parzibot Joins to Your Current Voice Channel\n'
                    ' - **/leave** - Parzibot Leaves Your Current Voice Channel\n'
                    ' - **/musichelp** `command` - The List of Parzibot Music Commands\n'
                    ' - **/next** - Play The Next Song in The Playlist\n'
                    ' - **/pause** - Pause The Current Song\n'
                    ' - **/play** `url` - Play The Song in The Current Voice Channel\n'
                    ' - **/playlist** - The Number of Songs in The Playlist\n'
                    ' - **/replay** - Replay The Current Song\n'
                    ' - **/resume** - Resume The Current Song\n'
                    ' - **/shuffle** - Shuffle The Playlist of Songs\n'
                    ' - **/stop** - Stop The Current Song'),
                color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        elif command == "clearplaylist":
            embed=Embed(
                title="**/clearplaylist** command - Clear Music Playlist",
                description=('**Syntax:** **/clearplaylist**'),
                color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        elif command == "join":
            embed=Embed(
                title="**/join** command - Parzibot Joins to Your Current Voice Channel",
                description=('**Syntax:** **/join**'),
                color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        elif command == "leave":
            embed=Embed(
                title="**/leave** command - Parzibot Leaves Your Current Voice Channel",
                description=('**Syntax:** **/leave**'),
                color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        elif command == "musichelp":
            embed=Embed(
                title="**/musichelp** command - The List of Parzibot Music Commands",
                description=(
                    '**Syntax:** **/musichelp** `command`\n'
                    '**Options:** `command` - The Help Message for Specific Music Command **(Optional)**'),
                color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        elif command == "next":
            embed=Embed(
                title="**/next** command - Play The Next Song in The Playlist",
                description=('**Syntax:** **/next**'),
                color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        elif command == "pause":
            embed=Embed(
                title="**/pause** command - Pause The Current Song",
                description=('**Syntax:** **/pause**'),
                color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        elif command == "play":
            embed=Embed(
                title="**/play** command - Play The Song in The Current Voice Channel",
                description=(
                    '**Syntax:** **/play** `url`\n'
                    '**Options:** `url` - YouTube Video URL **(Required)**'
                    ),
                color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        elif command == "playlist":
            embed=Embed(
                title="**/playlist** command - The Number of Songs in The Playlist",
                description=('**Syntax:** **/playlist**'),
                color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        elif command == "replay":
            embed=Embed(
                title="**/replay** command - Replay The Current Song",
                description=('**Syntax:** **/replay**'),
                color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        elif command == "resume":
            embed=Embed(
                title="**/resume** command - Resume The Current Song",
                description=('**Syntax:** **/resume**'),
                color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        elif command == "shuffle":
            embed=Embed(
                title="**/shuffle** command - Shuffle The List of Songs",
                description=('**Syntax:** **/shuffle**'),
                color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        elif command == "stop":
            embed=Embed(
                title="**/stop** command - Stop The Current Song",
                description=('**Syntax:** **/stop**'),
                color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)

    @cog_ext.cog_slash(name="next", description="Play The Next Song in The Playlist")
    async def next(self, ctx):
        """Play The Next Song in The Playlist"""
        if (
            ctx.author.voice is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            embed=Embed(title="**Parzibot** isn't connected to your **Voice Channel**", color=Colour(0xff6868))
            embed.set_thumbnail(url="attachment://ParzibotError.png")
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"), embed=embed)
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()
        if self.songs: await self.play_song(ctx)
        else:
            embed=Embed(title="**The Playlist** is empty", color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)

    @cog_ext.cog_slash(name="pause", description="Pause The Current Song")
    async def pause(self, ctx):
        """Pause The Current Song"""
        if ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel:
            embed=Embed(title="**Parzibot** isn't connected to your **Voice Channel**", color=Colour(0xff6868))
            embed.set_thumbnail(url="attachment://ParzibotError.png")
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"), embed=embed)
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
            embed=Embed(title="**The Song** has been paused", color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        else:
            embed=Embed(title="**The Song** isn't playing right now", color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)


    @cog_ext.cog_slash(
        name="play",
        description="Play The Song in The Current Voice Channel",
        options=[
            create_option(
                name="url",
                description="YouTube Video URL",
                option_type=3,
                required=True
                )
            ])
    async def play(self, ctx, url: str):
        """Play The Song in The Current Voice Channel"""
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if (
            ctx.author.voice is None or voice is not None and ctx.author.voice.channel != ctx.voice_client.channel
        ):
            embed=Embed(title="**Parzibot** isn't connected to your **Voice Channel**", color=Colour(0xff6868))
            embed.set_thumbnail(url="attachment://ParzibotError.png")
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"), embed=embed)

        self.songs.append(str(url))

        channel = ctx.author.voice.channel
        if channel and channel is not None:
            if voice is not None and voice.is_connected() is not None: 
                await voice.move_to(channel)
            else:  voice = await channel.connect()

            if not voice.is_playing() or voice.is_paused(): 
                await self.play_song(ctx)
            else:
                embed=Embed(
                    title="**The Song** added to playlist",
                    description="If you want to play song right now write **/next**",
                    color=Colour(0x68FFD9))
                embed.set_thumbnail(url="attachment://Parzibot.png")
                await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        else:
            embed=Embed(title="You're not connected to any **Voice Channel**", color=Colour(0xff6868))
            embed.set_thumbnail(url="attachment://ParzibotError.png")
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"), embed=embed)

    async def play_song(self, ctx):
        def search(url):
            with youtube_dl.YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True'}) as ydl:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
            return {'source': info['formats'][0]['url'], 'title': info['title']}

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if self.songs:
            self.current = self.songs.pop(0)
            data = search(self.current)
            
            voice.play(discord.FFmpegPCMAudio(data['source'], **self.FFMPEG_OPTIONS),
                       after=lambda e: asyncio.run_coroutine_threadsafe(self.play_song(ctx), self.client.loop))
            
            voice.is_playing()
            embed=Embed(title=f"**{data['title']}** is playing now", color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)

    @cog_ext.cog_slash(name="playlist", description="The Number of Songs in The Playlist")
    async def playlist(self, ctx):
        """The Number of Songs in The Playlist"""
        if (
            ctx.author.voice is None or ctx.voice_client is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            embed=Embed(title="**Parzibot** isn't connected to your **Voice Channel**", color=Colour(0xff6868))
            embed.set_thumbnail(url="attachment://ParzibotError.png")
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"), embed=embed)
            return
        if self.songs:
            embed=Embed(title=f"**The Playlist** contains about **{len(self.songs)}** song(-s)", color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        else:
            embed=Embed(title="**The Playlist** is empty", color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)

    @cog_ext.cog_slash(name="replay", description="Replay The Current Song")
    async def replay(self, ctx):
        """Replay The Current Song"""
        if (
            ctx.author.voice is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            embed=Embed(title="**Parzibot** isn't connected to your **Voice Channel**", color=Colour(0xff6868))
            embed.set_thumbnail(url="attachment://ParzibotError.png")
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"), embed=embed)
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()

        await self.replay_song(ctx)

    async def replay_song(self, ctx):
        def search(url):
            with youtube_dl.YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True'}) as ydl:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
            return {'source': info['formats'][0]['url'], 'title': info['title']}

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        data = search(self.current)
        voice.play(discord.FFmpegPCMAudio(data['source'], **self.FFMPEG_OPTIONS),
            after=lambda e: asyncio.run_coroutine_threadsafe(self.play_song(ctx), self.client.loop))
        
        voice.is_playing()
        embed=Embed(title=f"**{data['title']}** is playing now", color=Colour(0x68FFD9))
        embed.set_thumbnail(url="attachment://Parzibot.png")
        await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)

    @cog_ext.cog_slash(name="resume", description="Resume The Current Song")
    async def resume(self, ctx):
        """Resume The Current Song"""
        if ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel:
            embed=Embed(title="**Parzibot** isn't connected to your **Voice Channel**", color=Colour(0xff6868))
            embed.set_thumbnail(url="attachment://ParzibotError.png")
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"), embed=embed)
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
            embed=Embed(title="**The Song** has been resumed", color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        else:
            embed=Embed(title="**The Song** isn't paused", color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)

    @cog_ext.cog_slash(name="shuffle", description="Shuffle The Playlist of Songs")
    async def shuffle(self, ctx):
        """Shuffle The Playlist of Songs"""
        if (
            ctx.author.voice is None
                or ctx.author.voice.channel != ctx.voice_client.channel
        ):
            embed=Embed(title="**Parzibot** isn't connected to your **Voice Channel**", color=Colour(0xff6868))
            embed.set_thumbnail(url="attachment://ParzibotError.png")
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"), embed=embed)
            return
        elif self.songs:
            random.shuffle(self.songs)
            embed=Embed(title=f"**The Playlist** has been shuffled", color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)
        else:
            embed=Embed(title=f"**The Playlist** is empty", color=Colour(0x68FFD9))
            embed.set_thumbnail(url="attachment://Parzibot.png")
            await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)

    @cog_ext.cog_slash(name="stop", description="Stop The Current Song")
    async def stop(self, ctx):
        """Stop The Current Song"""
        if ctx.author.voice is None or ctx.author.voice.channel != ctx.voice_client.channel:
            embed=Embed(title="**Parzibot** isn't connected to your **Voice Channel**", color=Colour(0xff6868))
            embed.set_thumbnail(url="attachment://ParzibotError.png")
            await ctx.send(file=discord.File("images/ParzibotError.png", filename="ParzibotError.png"), embed=embed)
            return
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice.stop()
        embed=Embed(title=f"**The Song** has been stopped", color=Colour(0x68FFD9))
        embed.set_thumbnail(url="attachment://Parzibot.png")
        await ctx.send(file=discord.File("images/Parzibot.png", filename="Parzibot.png"), embed=embed)


def setup(client):
    """Setup function"""
    client.add_cog(Music(client))
