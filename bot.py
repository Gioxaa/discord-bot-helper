import discord
from discord.ext import commands
import asyncio
import json
import os
import datetime


# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

# Bot setup with intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config['prefix'], intents=intents)
bot.remove_command('help')

def has_buyer_role(ctx):
    user_roles = [role.id for role in ctx.author.roles]
    return any(role_id in user_roles for role_id in config['buyer_roles'])

async def userinfo(ctx):
    user_id = ctx.author.id

def get_current_time():
  now = datetime.datetime.now()
  current_time = now.strftime("%H:%M:%S")
  return current_time

def whoami(ctx):
    user_name = ctx.author.name
    user_display_name = ctx.author.display_name
    
def clear():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Others
        os.system('clear')

# Event when bot is ready
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Melayani Customer"))
    clear()
    print(f"{config['bot_name']} is online!")
    os.system("title SUPPORT BOT BY GIOXA") 
    

# Command: .start
@bot.command()
async def start(ctx):
    if has_buyer_role(ctx):
        response = (
            "Untuk claim garansi atau masalah produk digital Anda, "
            "silakan pilih kategori produk yang sesuai dan gunakan command yang tersedia:\n"
            ".canvagaransi - Claim garansi untuk Canva\n"
            ".netflixgaransi - Claim garansi untuk Netflix\n"
            ".spotifygaransi - Claim garansi untuk Spotify\n"
            ".otherapp - Claim garansi untuk aplikasi lainnya"
        )
        await ctx.send(response)
    else:
        await ctx.send("Anda tidak memiliki izin untuk menggunakan command ini.")

# Command: .canvagaransi
@bot.command()
async def canvagaransi(ctx):
    if has_buyer_role(ctx):
        await ctx.send("FORMAT CANVA\n\nEmail: \nDesainer/Member: \nDurasi Order: \n\n**WAJIB MENGGUNAKAN FORMAT INI**")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel
        
        while True:
            try:
                msg = await bot.wait_for('message', check=check, timeout=300.0)

                if "FORMAT CANVA" in msg.content.upper():
                    # Kirim pesan konfirmasi dan tambahkan reaksi
                    confirm_message = await ctx.send("Apakah format sudah benar? Silakan konfirmasi.")
                    await confirm_message.add_reaction('✅')  # Tambahkan reaksi ✅
                    await confirm_message.add_reaction('❌')  # Tambahkan reaksi ❌

                    # Tunggu reaksi dari pengguna
                    def confirm_check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) in ['✅', '❌'] and reaction.message == confirm_message

                    try:
                        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=confirm_check)

                        if str(reaction.emoji) == '✅':  # Jika pengguna memilih ✅
                            report_channel = bot.get_channel(config['report_channel_id'])
                            await report_channel.send(f"<@939756275561025577>\n# GARANSI CANVA\nUser: <@{user.id}>\n```{msg.content}```")
                            await ctx.send("Support akan membantu segera!")
                            print(f"[LOG] {ctx.author.display_name} Ingin Claim Garansi Canva, Cek Server!")
                        else:  # Jika pengguna memilih ❌
                            await ctx.send("Silakan perbaiki format dan kirim ulang.")
                            continue

                    except asyncio.TimeoutError:
                        await ctx.send("Waktu konfirmasi habis. Silakan ulangi proses.")

                    break  # Keluar dari loop setelah konfirmasi

                else:
                    await ctx.send("Format salah. Harap gunakan format yang benar: FORMAT CANVA")

            except discord.TimeoutError:
                await ctx.send("Waktu habis. Silakan ulangi command ini jika Anda ingin claim garansi.")

    else:
        await ctx.send("Anda tidak memiliki izin untuk menggunakan command ini.")

# Command: .netflixgaransi
@bot.command()
async def netflixgaransi(ctx):
    if has_buyer_role(ctx):
        await ctx.send("FORMAT NETFLIX\nEmail: ")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        while True:
            try:
                msg = await bot.wait_for('message', check=check, timeout=300.0)

                if "FORMAT NETFLIX" in msg.content.upper():
                    # Kirim pesan konfirmasi dan tambahkan reaksi
                    confirm_message = await ctx.send("Apakah format sudah benar? Silakan konfirmasi.")
                    await confirm_message.add_reaction('✅')  # Tambahkan reaksi ✅
                    await confirm_message.add_reaction('❌')  # Tambahkan reaksi ❌

                    # Tunggu reaksi dari pengguna
                    def confirm_check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) in ['✅', '❌'] and reaction.message == confirm_message

                    try:
                        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=confirm_check)

                        if str(reaction.emoji) == '✅':  # Jika pengguna memilih ✅
                            report_channel = bot.get_channel(config['report_channel_id'])
                            await report_channel.send(f"Garansi Aplikasi Lain:\nUser: {ctx.author}\nEmail: {msg.content}")
                            await ctx.send("Support akan membantu segera!")
                            print(f"[LOG] {ctx.author.display_name} Ingin Claim Garansi Netflix, Cek Server!")
                        else:  # Jika pengguna memilih ❌
                            await ctx.send("Silakan perbaiki format dan kirim ulang.")
                            continue

                    except asyncio.TimeoutError:
                        await ctx.send("Waktu konfirmasi habis. Silakan ulangi proses.")

                    break  # Keluar dari loop setelah konfirmasi

                else:
                    await ctx.send("Format salah. Harap gunakan format yang benar: FORMAT NETFLIX")

            except discord.TimeoutError:
                await ctx.send("Waktu habis. Silakan ulangi command ini jika Anda ingin claim garansi.")

    else:
        await ctx.send("Anda tidak memiliki izin untuk menggunakan command ini.")

# Command: .spotifygaransi
@bot.command()
async def spotifygaransi(ctx):
    if has_buyer_role(ctx):
        await ctx.send("FORMAT SPOTIFY\nEmail: ")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        while True:
            try:
                msg = await bot.wait_for('message', check=check, timeout=300.0)

                if "FORMAT SPOTIFY" in msg.content.upper():
                    # Kirim pesan konfirmasi dan tambahkan reaksi
                    confirm_message = await ctx.send("Apakah format sudah benar? Silakan konfirmasi.")
                    await confirm_message.add_reaction('✅')  # Tambahkan reaksi ✅
                    await confirm_message.add_reaction('❌')  # Tambahkan reaksi ❌

                    # Tunggu reaksi dari pengguna
                    def confirm_check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) in ['✅', '❌'] and reaction.message == confirm_message

                    try:
                        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=confirm_check)

                        if str(reaction.emoji) == '✅':  # Jika pengguna memilih ✅
                            report_channel = bot.get_channel(config['report_channel_id'])
                            await report_channel.send(f"Garansi Aplikasi Lain:\nUser: {ctx.author}\nEmail: {msg.content}")
                            await ctx.send("Support akan membantu segera!")
                            print(f"[LOG] {ctx.author.display_name} Ingin Claim Garansi Spotify, Cek Server!")
                        else:  # Jika pengguna memilih ❌
                            await ctx.send("Silakan perbaiki format dan kirim ulang.")
                            continue

                    except asyncio.TimeoutError:
                        await ctx.send("Waktu konfirmasi habis. Silakan ulangi proses.")

                    break  # Keluar dari loop setelah konfirmasi

                else:
                    await ctx.send("Format salah. Harap gunakan format yang benar: FORMAT SPOTIFY")

            except discord.TimeoutError:
                await ctx.send("Waktu habis. Silakan ulangi command ini jika Anda ingin claim garansi.")

    else:
        await ctx.send("Anda tidak memiliki izin untuk menggunakan command ini.")


# Command: .otherapp
@bot.command()
async def otherapp(ctx):
    if has_buyer_role(ctx):
        await ctx.send("FORMAT APLIKASI LAIN\nEmail: ")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        while True:
            try:
                msg = await bot.wait_for('message', check=check, timeout=300.0)

                if "FORMAT APLIKASI LAIN" in msg.content.upper():
                    # Kirim pesan konfirmasi dan tambahkan reaksi
                    confirm_message = await ctx.send("Apakah format sudah benar? Silakan konfirmasi.")
                    await confirm_message.add_reaction('✅')  # Tambahkan reaksi ✅
                    await confirm_message.add_reaction('❌')  # Tambahkan reaksi ❌

                    # Tunggu reaksi dari pengguna
                    def confirm_check(reaction, user):
                        return user == ctx.author and str(reaction.emoji) in ['✅', '❌'] and reaction.message == confirm_message

                    try:
                        reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=confirm_check)

                        if str(reaction.emoji) == '✅':  # Jika pengguna memilih ✅
                            report_channel = bot.get_channel(config['report_channel_id'])
                            await report_channel.send(f"Garansi Aplikasi Lain:\nUser: {ctx.author}\nEmail: {msg.content}")
                            await ctx.send("Support akan membantu segera!")
                            print(f"[LOG] {ctx.author.display_name} Ingin Claim Garansi Aplikasi Lain, Cek Server!")
                        else:  # Jika pengguna memilih ❌
                            await ctx.send("Silakan perbaiki format dan kirim ulang.")
                            continue

                    except asyncio.TimeoutError:
                        await ctx.send("Waktu konfirmasi habis. Silakan ulangi proses.")

                    break  # Keluar dari loop setelah konfirmasi

                else:
                    await ctx.send("Format salah. Harap gunakan format yang benar: FORMAT APLIKASI LAIN")

            except discord.TimeoutError:
                await ctx.send("Waktu habis. Silakan ulangi command ini jika Anda ingin claim garansi.")

    else:
        await ctx.send("Anda tidak memiliki izin untuk menggunakan command ini.")

# Run the bot
bot.run(config['token'])
