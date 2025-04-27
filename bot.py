import os
import asyncio
import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from scrapers.milanuncios import buscar_milanuncios
from scrapers.wallapop import buscar_wallapop
from scrapers.autocasion import buscar_autocasion
from scrapers.autoscout24 import buscar_autoscout24

TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print("❌ No se encontró el TOKEN de Telegram.")
    exit(1)

MODELOS = ['rifter', 'berlingo combi', 'tourneo courier', 'doblo']
PRECIO_MIN = 4000
PRECIO_MAX = 12000

async def buscar_ofertas(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data['chat_id']

    await context.bot.send_message(chat_id=chat_id, text="🔍 Buscando ofertas...")

    resultados = []

    try:
        resultados += buscar_milanuncios(MODELOS, PRECIO_MIN, PRECIO_MAX)
        resultados += await buscar_wallapop(MODELOS, PRECIO_MIN, PRECIO_MAX)
        resultados += await buscar_autocasion(MODELOS, PRECIO_MIN, PRECIO_MAX)
        resultados += await buscar_autoscout24(MODELOS, PRECIO_MIN, PRECIO_MAX)
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"⚠️ Error buscando ofertas: {e}")
        return

    if not resultados:
        await context.bot.send_message(chat_id=chat_id, text="❌ No se han encontrado ofertas nuevas esta vez.")
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"✅ {len(resultados)} ofertas encontradas. Enviando...")
        for oferta in resultados:
            await context.bot.send_message(chat_id=chat_id, text=oferta['titulo'] + "\n" + oferta['precio'] + "\n" + oferta['url'])
            await asyncio.sleep(2)

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    await context.bot.send_message(chat_id=chat_id, text="🤖 Bot activado. Buscaré ofertas cada 10 minutos.")

    context.application.job_queue.run_repeating(
        buscar_ofertas,
        interval=600,
        first=10,
        data={'chat_id': chat_id}
    )

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))

    print("✅ Bot iniciado...")
    await app.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
