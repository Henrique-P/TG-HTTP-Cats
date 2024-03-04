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
            )
        )
    await update.inline_query.answer(results)

if __name__ == '__main__':
    application = ApplicationBuilder().token(token).build()
    application.add_handler(InlineQueryHandler(inline_cat, r'([1-5]\d\d?$)'))
    application.run_polling()