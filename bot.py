import os
import asyncio
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler
from scrapers.milanuncios import buscar_milanuncios
from scrapers.cochesnet import buscar_cochesnet
from scrapers.wallapop import buscar_wallapop
from scrapers.autocasion import buscar_autocasion
from scrapers.autoscout24 import buscar_autoscout24
from utils.formatting import formatear_mensaje

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    print("ERROR: No se encontró el TOKEN de Telegram.")
    exit(1)

CHAT_ID = ''

MODELOS = ['rifter', 'berlingo combi', 'tourneo courier', 'doblo']
PRECIO_MIN = 4000
PRECIO_MAX = 12000

bot = Bot(token=TOKEN)

async def buscar_ofertas():
    global CHAT_ID
    resultados = []

    resultados += buscar_milanuncios(MODELOS, PRECIO_MIN, PRECIO_MAX)
    resultados += buscar_cochesnet(MODELOS, PRECIO_MIN, PRECIO_MAX)
    resultados += await buscar_wallapop(MODELOS, PRECIO_MIN, PRECIO_MAX)
    resultados += await buscar_autocasion(MODELOS, PRECIO_MIN, PRECIO_MAX)
    resultados += await buscar_autoscout24(MODELOS, PRECIO_MIN, PRECIO_MAX)

    if not resultados:
        if CHAT_ID:
            await bot.send_message(chat_id=CHAT_ID, text="No se han encontrado ofertas nuevas.")
    else:
        for oferta in resultados:
            if CHAT_ID:
                await bot.send_message(chat_id=CHAT_ID, text=formatear_mensaje(oferta))
            await asyncio.sleep(2)

async def start(update, context):
    global CHAT_ID
    CHAT_ID = update.message.chat_id
    await context.bot.send_message(chat_id=CHAT_ID, text="¡Bot activado! Buscaré cada 10 minutos.")
    await buscar_ofertas()

async def periodic_search(app):
    while True:
        await buscar_ofertas()
        await asyncio.sleep(600)  # 10 minutos

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))

    asyncio.create_task(periodic_search(app))

    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.stop()
