import os
import asyncio
from aiohttp import web
from dotenv import load_dotenv
from discord.ext import commands
import discord

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# --- Discord intents (bezpiecznie) ---
intents = discord.Intents.default()
intents.message_content = True  # włącz Message Content Intent w Developer Portal jeśli używasz treści wiadomości

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Zalogowano jako {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

@bot.command()
async def hello(ctx):
    await ctx.send("👋 Cześć!")

# --- mały webserver, żeby Render widział otwarty port ---
async def handle_root(request):
    return web.Response(text="Bot is running. ✅")

async def start_webserver():
    port = int(os.environ.get("PORT", 8000))  # Render ustawia PORT automatycznie
    app = web.Application()
    app.add_routes([web.get('/', handle_root)])
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server started on port {port}")

# --- uruchomienie: jednocześnie webserver + discord bot ---
async def main():
    # start webserver w tle
    await start_webserver()
    # start bota (zawiesi event loop)
    await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Shutting down")
