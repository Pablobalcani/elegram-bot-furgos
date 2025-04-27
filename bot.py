import os
import asyncio
import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv('TOKEN')

if not TOKEN:
    print("❌ No se encontró el TOKEN de Telegram.")
    exit(1)

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('🤖 Bot activado y listo.')

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))

    print("✅ Bot iniciado...")
    await app.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
