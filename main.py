import logging
from telegram import InlineQueryResultPhoto, Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, InlineQueryHandler, CommandHandler
from helper import codeIsValid, randomCode, codeMatches
from telegramToken import token

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)               

async def inline_cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    for option in codeMatches(query):
        results.append(
            InlineQueryResultPhoto(
            id = option,
            thumbnail_url = f"https://http.cat/{option}",
            photo_url = f"https://http.cat/{option}",
            title = option
            )
        )
    await update.inline_query.answer(results)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi!\nCurrently there are no funcions for this bot.\nTry calling me inline with a HTTP Code!")
    
if __name__ == '__main__':
    app = ApplicationBuilder().token(token).build()
    app.add_handler(InlineQueryHandler(inline_cat, r'([1-5]\d\d?$)'))
    app.add_handler(CommandHandler('start', start))
    app.run_polling()