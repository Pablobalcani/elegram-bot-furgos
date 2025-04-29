import os
import asyncio
import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from scrapers.milanuncios import buscar_milanuncios
from scrapers.wallapop import buscar_wallapop
from scrapers.autocasion import buscar_autocasion
from scrapers.autoscout24 import buscar_autoscout24
from scrapers.cochesnet import buscar_cochesnet
from utils.formatting import formatear_mensaje

TOKEN = os.getenv('TOKEN')

MODELOS = ['rifter', 'berlingo combi', 'tourneo courier', 'doblo']

MODELOS_COCHESNET = {
    'rifter': (33, 1252),
    'berlingo combi': (15, 1127),
    'tourneo courier': (14, 694),
    'doblo': (23, 868)
}

PRECIO_MIN = 4000
PRECIO_MAX = 18000

async def buscar_ofertas(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data['chat_id']
    await context.bot.send_message(chat_id=chat_id, text="🔍 Buscando ofertas...")

    resultados = []

    try:
        resultados += await buscar_milanuncios(MODELOS, PRECIO_MIN, PRECIO_MAX)
        resultados += await buscar_cochesnet(MODELOS_COCHESNET, PRECIO_MIN, PRECIO_MAX)
        resultados += await buscar_wallapop(MODELOS, PRECIO_MIN, PRECIO_MAX)
        resultados += await buscar_autocasion(MODELOS, PRECIO_MIN, PRECIO_MAX)
        resultados += await buscar_autoscout24(MODELOS, PRECIO_MIN, PRECIO_MAX)
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"⚠️ Error buscando ofertas: {e}")
        return

    if not resultados:
        await context.bot.send_message(chat_id=chat_id, text="❌ No se han encontrado ofertas nuevas.")
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"✅ {len(resultados)} ofertas encontradas. Enviando...")
        for oferta in resultados:
            await context.bot.send_message(chat_id=chat_id, text=formatear_mensaje(oferta))
            await asyncio.sleep(2)

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text="🤖 Bot activado. Buscaré ofertas cada 10 minutos.")

    context.job_queue.run_repeating(
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
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "already running" in str(e):
            nest_asyncio.apply()
            loop = asyncio.get_event_loop()
            loop.create_task(main())
            loop.run_forever()
        else:
            raise
