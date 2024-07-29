import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import os

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Giriş yapıldı olarak: {bot.user}')

@bot.command(name='play')
async def play(ctx, url):
    if ctx.author.voice is None:
        await ctx.send("Önce bir sesli kanala katılmalısınız!")
        return

    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'temp_audio.%(ext)s'
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            audio_file = ydl.prepare_filename(info)

        ffmpeg_opts = {
            'executable': 'C:\\ffmpeg\\bin\\ffmpeg.exe',
            'options': '-vn'
        }
        source = discord.FFmpegPCMAudio(audio_file, **ffmpeg_opts)
        
        def after_playing(error):
            if error:
                print(f"Oynatma hatası: {error}")
            if os.path.exists(audio_file):
                os.remove(audio_file)
                print(f"{audio_file} dosyası silindi.")

        ctx.voice_client.play(source, after=after_playing)
        await ctx.send("Ses akışı başlatıldı!")
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {e}")
        print(f"Bir hata oluştu: {e}")

TOKEN = 'your_token'
bot.run(TOKEN)
