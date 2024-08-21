import discord
from discord.ext import commands
import asyncio
import json
import os
import datetime
import random

# Load configuration
with open('config.json') as config_file:
    config = json.load(config_file)

# Load stock data
def load_stock():
    if not os.path.exists('stock.json'):
        with open('stock.json', 'w') as file:
            json.dump({
                "netflix": 0,
                "canva": 0,
                "youtube": 0,
                "vidio": 0,
                "iqiyi": 0,
                "capcut": 0,
                "amazon-prime-video": 0,
                "we-tv": 0,
                "bstation": 0,
                "spotify": 0,
                "get-contact": 0,
                "zoom-meeting": 0
            }, file)
    with open('stock.json') as file:
        return json.load(file)

def save_stock(stock):
    with open('stock.json', 'w') as file:
        json.dump(stock, file, indent=4)

# Bot setup with intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config['prefix'], intents=intents)
bot.remove_command('help')

def has_buyer_role(ctx):
    user_roles = [role.id for role in ctx.author.roles]
    return any(role_id in user_roles for role_id in config['buyer_roles'])

def is_admin(ctx):
    user_roles = [role.id for role in ctx.author.roles]
    return any(role_id in user_roles for role_id in config['admin_roles'])

def get_current_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

async def handle_warranty(ctx, format_name, expected_format):
    if not has_buyer_role(ctx):
        await ctx.send("Anda tidak memiliki izin untuk menggunakan command ini.")
        return

    await ctx.send(f"{expected_format}\n\n**WAJIB MENGGUNAKAN FORMAT INI**\nKetik 'cancel' untuk membatalkan proses.")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    while True:
        try:
            msg = await bot.wait_for('message', check=check, timeout=300.0)

            if msg.content.lower() == 'cancel':
                await ctx.send("Proses garansi dibatalkan.")
                print(f"[LOG] {ctx.author.display_name} membatalkan proses garansi {format_name}.")
                return  # Exit the function to end the process

            if format_name in msg.content.upper():
                confirm_message = await ctx.send("Apakah format sudah benar? Silakan konfirmasi.")
                await confirm_message.add_reaction('✅')
                await confirm_message.add_reaction('❌')

                def confirm_check(reaction, user):
                    return user == ctx.author and str(reaction.emoji) in ['✅', '❌'] and reaction.message == confirm_message

                try:
                    reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=confirm_check)

                    if str(reaction.emoji) == '✅':
                        report_channel = bot.get_channel(config['report_channel_id'])
                        await report_channel.send(f"<@939756275561025577>\n# GARANSI {format_name.upper()}\nUser: <@{user.id}>\n```{msg.content}```")
                        await ctx.send("Support akan membantu segera!")
                        print(f"[LOG] {ctx.author.display_name} Ingin Claim Garansi {format_name}, Cek Server!")
                    else:
                        await ctx.send("Silakan perbaiki format dan kirim ulang.")
                        continue

                except asyncio.TimeoutError:
                    await ctx.send("Waktu konfirmasi habis. Silakan ulangi proses.")
                
                break
            else:
                await ctx.send(f"Format salah. Harap gunakan format yang benar: {expected_format}")

        except discord.TimeoutError:
            await ctx.send("Waktu habis. Silakan ulangi command ini jika Anda ingin claim garansi.")

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
        embed = discord.Embed(
            title="🏆 **GARANSI COMMAND**",
            # description="Silakan pilih kategori produk yang sesuai dan gunakan command yang tersedia:",
            color=discord.Color.from_rgb(255, 223, 0)
        )
        
        # Adding fields to the embed
        embed.add_field(
            name="",
            value=(
                "Silakan pilih kategori produk yang sesuai dan gunakan command yang tersedia:\n\n"
                "**.canvagaransi** - Claim garansi untuk Canva\n"
                "**.netflixgaransi** - Claim garansi untuk Netflix\n"
                "**.spotifygaransi** - Claim garansi untuk Spotify\n"
                "**.otherapp** - Claim garansi untuk aplikasi lainnya"
            ),
            inline=False
        )

        # embed.add_field(
        #     name=":red_circle: Platinum",
        #     value=(
        #         "Bagi yang ingin menonton BRI Liga 1 2022, BRI Liga 2, UCL, IBL, serial Korea, "
        #         "maka bisa menggunakan layanan ini."
        #     ),
        #     inline=False
        # )

        # Adding an image to the embed
        embed.set_image(url="https://message.style/cdn/images/ba4c3c8870e2812c94ab6a3768de7aa519d74adb38c70fa027e8c4ec85e2b1de.gif")  # Replace with your image URL

        # Sending the embed
        await ctx.send(embed=embed)
    else:
        await ctx.send("Anda tidak memiliki izin untuk menggunakan command ini.")



# Command handlers for each warranty type
@bot.command()
async def canvagaransi(ctx):
    await handle_warranty(ctx, "CANVA", "FORMAT CANVA\n\nEmail: \nDesainer/Member: \nDurasi Order: ")

@bot.command()
async def netflixgaransi(ctx):
    await handle_warranty(ctx, "NETFLIX", "FORMAT NETFLIX\nEmail: ")

@bot.command()
async def spotifygaransi(ctx):
    await handle_warranty(ctx, "SPOTIFY", "FORMAT SPOTIFY\nEmail: ")

@bot.command()
async def otherapp(ctx):
    await handle_warranty(ctx, "APLIKASI LAIN", "FORMAT APLIKASI LAIN\nEmail: ")

# User Commands
@bot.command()
async def help(ctx):  
    embed = discord.Embed(
            title=":clipboard: **Help Command**",
            description=(
                "Berikut adalah daftar command yang tersedia:\n"
                ".help - Menampilkan semua command\n"
                ".stok - Mengecek stok seluruh barang\n"
                ".stok (appname) - Mengecek stok untuk aplikasi tertentu\n"
                ".payment - Menampilkan metode pembayaran yang diterima\n"
                ".snkappprem - Menampilkan syarat dan ketentuan aplikasi premium\n"
                ".payment - Menampilkan Payment apa saja yang di terima oleh Seller\n"
                
            ),
            color=discord.Color.from_rgb(255, 223, 0)
        )
    embed.add_field(
            name="**Admin Command:**",
            value=(
                "\n.addstok (appname) (amount)\n"
                ".removestock (app) (count) - Menghapus stok untuk aplikasi\n"
                ""
            ),
            inline=False
        )
    embed.set_image(url="https://message.style/cdn/images/ba4c3c8870e2812c94ab6a3768de7aa519d74adb38c70fa027e8c4ec85e2b1de.gif")

        # Sending the embed
    await ctx.send(embed=embed)


@bot.command()
async def stok(ctx, app=None):
    stock = load_stock()
    if app:
        app = app.lower()
        if app in stock:
            await ctx.send(f"Stok untuk {app.capitalize()}: {stock[app]}")
        else:
            await ctx.send("Aplikasi tidak ditemukan.")
    else:
        response = "\n".join([f"{app.capitalize()}: {count}" for app, count in stock.items()])
        embed = discord.Embed(
            title=":clipboard: **STOCK PRODUCT**",
            description=(
                f"{response}"
                
            ),
            color=discord.Color.from_rgb(255, 223, 0)
        )
        await ctx.send(embed=embed)
        

@bot.command()
async def payment(ctx):
    embed = discord.Embed(
            title=":credit_card: **PAYMENT**",
            description=(
                "*Payment Accept:*"
                "```" 
                "> DANA    ┃ 0822559997725 a/n Muhammad Reyhan\n"
                "> Gopay   ┃ 081258489742 a/n Muhammad Reyhan\n"
                "> SeaBank ┃ 901778459810 a/n Muhammad Reyhan\n"
                "```"
            ),
            color=discord.Color.from_rgb(255, 223, 0)
        )
    embed.add_field(
            name="**Note:**",
            value=(
                "- Untuk DANA apabila transfer melalu bank mana pun, wajib nominal transfer nya ditambah Rp500 dari harga awal. \n"
                "> -  Contoh buat transfer yang nominalnya wajib ditambah untuk dana: harga beli nya Rp50.000, tapi lu transfer nya melalui bank, bukan sesama ovo/dana, maka wajib dilebihin menjadi Rp50.500\n"
                "- Kirim Bukti Transfer Jika memesan Produk,\n"
                "- Tidak ada REFFUND jika sudah memesan, dan pesanan akan di proses."
            ),
            inline=False
    )
    await ctx.send(embed=embed)

@bot.command()
async def snkappprem(ctx):
    response = (
        "Syarat dan ketentuan untuk aplikasi premium:\n"
        "1. Anda harus memiliki akun yang valid.\n"
        "2. Stok terbatas, dan tidak dapat diganti setelah dibeli.\n"
        "3. Tidak ada pengembalian uang."
    )
    await ctx.send(response)

@bot.command()
async def removestok(ctx, app, count: int):
    if not is_admin(ctx):
        await ctx.send("Anda tidak memiliki izin untuk menggunakan command ini.")
        return
    
    stock = load_stock()
    app = app.lower()
    if app in stock:
        old_amount = stock[app]
        stock[app] = max(0, stock[app] - count)
        save_stock(stock)
        print(f"[LOG] {get_current_time()} - Pengurangan stok: {app.capitalize()} - Jumlah awal: {old_amount} - Jumlah yang dikurangi: {count} - Jumlah sekarang: {stock[app]}")
        await ctx.send(f"Stok untuk {app.capitalize()} telah diubah menjadi {stock[app]}.")
    else:
        await ctx.send("Aplikasi tidak ditemukan.")

# Admin Commands
@bot.command()
async def addstok(ctx, app, count: int):
    if not is_admin(ctx):
        await ctx.send("Anda tidak memiliki izin untuk menggunakan command ini.")
        return
    
    stock = load_stock()
    app = app.lower()
    if app in stock:
        old_amount = stock[app]
        stock[app] += count
        save_stock(stock)
        print(f"[LOG] {get_current_time()} - Penambahan stok: {app.capitalize()} - Jumlah awal: {old_amount} - Jumlah yang ditambahkan: {count} - Jumlah sekarang: {stock[app]}")
        await ctx.send(f"Stok untuk {app.capitalize()} telah ditambahkan menjadi {stock[app]}.")
    else:
        await ctx.send("Aplikasi tidak ditemukan.")

@bot.command()
async def gkick(ctx, user: discord.Member):
    if not is_admin(ctx):
        await ctx.send("Anda tidak memiliki izin untuk menggunakan command ini.")
        return
    
    try:
        await user.kick(reason="Kicked by admin")
        await ctx.send(f"{user.mention} telah dikick dari server.")
    except discord.Forbidden:
        await ctx.send("Bot tidak memiliki izin untuk mengkick pengguna. Pastikan bot memiliki izin 'Kick Members'.")
    except discord.HTTPException as e:
        await ctx.send(f"Terjadi kesalahan saat mencoba mengkick pengguna: {e}")
    except Exception as e:
        await ctx.send(f"Terjadi kesalahan yang tidak diketahui: {e}")

@bot.command()
async def gban(ctx, user: discord.Member, duration: str):
    if not is_admin(ctx):
        await ctx.send("Anda tidak memiliki izin untuk menggunakan command ini.")
        return
    
    try:
        # Convert duration to minutes if it is not permanent
        if duration == '-':
            await user.ban(reason="Banned by admin (Permanent)")
            await ctx.send(f"{user.mention} telah dibanned dari server secara permanen.")
        else:
            try:
                duration_minutes = int(duration)
                await user.ban(reason=f"Banned by admin for {duration_minutes} minutes")
                await ctx.send(f"{user.mention} telah dibanned dari server untuk {duration_minutes} menit.")
                
                # Schedule unban after the duration
                await asyncio.sleep(duration_minutes * 60)
                await ctx.guild.unban(user)
                await ctx.send(f"{user.mention} telah di-unban setelah {duration_minutes} menit.")
            except ValueError:
                await ctx.send("Durasi tidak valid. Harap masukkan durasi dalam menit.")
    
    except discord.Forbidden:
        await ctx.send("Bot tidak memiliki izin untuk membanned pengguna. Pastikan bot memiliki izin 'Ban Members'.")
    except discord.HTTPException as e:
        await ctx.send(f"Terjadi kesalahan saat mencoba membanned pengguna: {e}")
    except Exception as e:
        await ctx.send(f"Terjadi kesalahan yang tidak diketahui: {e}")

bot.run(config['token'])
