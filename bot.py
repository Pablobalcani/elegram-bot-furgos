
import logging
import schedule
import time
import os
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from scrapers.milanuncios import buscar_milanuncios
from scrapers.cochesnet import buscar_cochesnet

TOKEN = os.getenv('TOKEN')  # Leer token de variable de entorno
CHAT_ID = ''

MODELOS = ['rifter', 'berlingo', 'tourneo courier', 'doblo']
PRECIO_MIN = 3000
PRECIO_MAX = 8000

bot = Bot(token=TOKEN)

def buscar_ofertas():
    global CHAT_ID
    resultados = []
    resultados += buscar_milanuncios(MODELOS, PRECIO_MIN, PRECIO_MAX)
    resultados += buscar_cochesnet(MODELOS, PRECIO_MIN, PRECIO_MAX)

    if not resultados:
        if CHAT_ID:
            bot.send_message(chat_id=CHAT_ID, text="No se han encontrado ofertas nuevas esta vez.")
    else:
        for oferta in resultados:
            if CHAT_ID:
                bot.send_message(chat_id=CHAT_ID, text=oferta)
            time.sleep(2)

def start(update, context):
    global CHAT_ID
    CHAT_ID = update.message.chat_id
    context.bot.send_message(chat_id=CHAT_ID, text="¡Hola! Bot activado. Buscaré ofertas nuevas cada 10 minutos.")
    buscar_ofertas()

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))

    updater.start_polling()

    schedule.every(10).minutes.do(buscar_ofertas)

    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    main()
