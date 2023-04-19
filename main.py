import logging
from telegram import InlineQueryResultPhoto, Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler, InlineQueryHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    codeNumber = update.message.text
    if codeNumber.isdigit(): 
        codeNumber = int(codeNumber)
        if (codeNumber > 99 and codeNumber < 600):
            await update.message.reply_photo(f"https://http.cat/{codeNumber}")
    else:
        await update.message.reply_photo("https://http.cat/400")

async def inline_cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    if query.isdigit(): 
        codeNumber = int(query)
        if (codeNumber > 99 and codeNumber < 600):
            results = [
                InlineQueryResultPhoto(
                id = query,
                thumbnail_url = f"https://http.cat/{query}",
                photo_url = f"https://http.cat/{query}",
            )
            ]
            await update.inline_query.answer(results)
    else: 
        await update.message.reply_photo("https://http.cat/400")
if __name__ == '__main__':
    application = ApplicationBuilder().token('1925390535:AAE22472__rqBTMs0rMqkb9RkALO1P0oiWY').build()
    cat_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), cat)
    inline_cat_handler = InlineQueryHandler(inline_cat)
    application.add_handler(cat_handler)
    application.add_handler(inline_cat_handler)
    application.run_polling()