import os
import asyncio
import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# tus imports de scrapers...

TOKEN = os.getenv('TOKEN')

# Modelos...

async def buscar_ofertas(context: ContextTypes.DEFAULT_TYPE):
    # tu código de ofertas...

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
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .post_init(lambda app: app.job_queue)  # 👈 Esto es clave
        .build()
    )
    app.add_handler(CommandHandler('start', start))

    print("✅ Bot iniciado...")
    await app.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
