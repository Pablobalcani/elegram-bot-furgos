import asyncio
import logging
import schedule
import time
import os
import threading
from telegram import Bot
from telegram.ext import ApplicationBuilder, CommandHandler
from scrapers.milanuncios import buscar_milanuncios
from scrapers.cochesnet import buscar_cochesnet

TOKEN = os.getenv('TOKEN')
if not TOKEN:
    print("ERROR: No se encontró el TOKEN de Telegram. Configura la variable de entorno TOKEN.")
    exit(1)

CHAT_ID = ''

MODELOS = ['rifter', 'berlingo', 'tourneo courier', 'doblo']
PRECIO_MIN = 3000
PRECIO_MAX = 8000

bot = Bot(token=TOKEN)

async def buscar_ofertas():
    global CHAT_ID
    resultados = []
    resultados += buscar_milanuncios(MODELOS, PRECIO_MIN, PRECIO_MAX)
    resultados += buscar_cochesnet(MODELOS, PRECIO_MIN, PRECIO_MAX)

    if not resultados:
        if CHAT_ID:
            await bot.send_message(chat_id=CHAT_ID, text="No se han encontrado ofertas nuevas esta vez.")
    else:
        for oferta in resultados:
            if CHAT_ID:
                await bot.send_message(chat_id=CHAT_ID, text=oferta)
            await asyncio.sleep(2)

async def start(update, context):
    global CHAT_ID
    CHAT_ID = update.message.chat_id
    await context.bot.send_message(chat_id=CHAT_ID, text="¡Hola! Bot activado. Buscaré ofertas nuevas cada 10 minutos.")
    await buscar_ofertas()

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))

    schedule.every(10).minutes.do(buscar_ofertas)

    # Hilo para ejecutar schedule en segundo plano
    def run_schedule():
        while True:
            schedule.run_pending()
            time.sleep(30)

    threading.Thread(target=run_schedule, daemon=True).start()

    app.run_polling()

if __name__ == "__main__":
    main()
