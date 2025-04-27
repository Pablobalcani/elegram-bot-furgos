import os
import asyncio
import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from scrapers.milanuncios import buscar_milanuncios
from scrapers.cochesnet import buscar_cochesnet
from scrapers.wallapop import buscar_wallapop
from scrapers.autocasion import buscar_autocasion
from scrapers.autoscout24 import buscar_autoscout24
from utils.formatting import formatear_mensaje

TOKEN = os.getenv('TOKEN')

MODELOS = ['rifter', 'berlingo combi', 'tourneo courier', 'doblo']
PRECIO_MIN = 4000
PRECIO_MAX = 12000

async def buscar_ofertas(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data['chat_id']
    await context.bot.send_message(chat_id=chat_id, text="🔍 Buscando ofertas...")

    resultados = []

    try:
        resultados += await buscar_milanuncios(MODELOS, PRECIO_MIN, PRECIO_MAX)
        resultados += await buscar_cochesnet(MODELOS, PRECIO_MIN, PRECIO_MAX)
        resultados += await buscar_wallapop(MODELOS, PRECIO_MIN, PRECIO_MAX)
        resultados += await buscar_autocasion(MODELOS, PRECIO_MIN, PRECIO_MAX)
        resultados += await buscar_autoscout24(MODELOS, PRECIO_MIN, PRECIO_MAX)
    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"⚠️ Error buscando ofertas: {e}")
        return

    if not resultados:
        await context.bot.send_message(chat_id=chat_id, text="❌ No se han encontrado ofertas nuevas esta vez.")
    else:
        await context.bot.send_message(chat_id=chat_id, text=f"✅ {len(resultados)} ofertas encontradas. Envi_
