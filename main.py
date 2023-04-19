import logging
from telegram import InlineQueryResultPhoto, Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, InlineQueryHandler
from helper import telegramToken, codeIsValid, randomCode

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    codeNumber = update.message.text
    if (codeIsValid(codeNumber)):
        await update.message.reply_photo(f"https://http.cat/{codeNumber}")
    else:
       await update.message.reply_text(text="This code does not exist. Here's a random one instead:")
       await update.message.reply_photo(f"https://http.cat/{randomCode()}")
                

async def inline_cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = [
        InlineQueryResultPhoto(
        id = query,
        thumbnail_url = f"https://http.cat/{query}",
        photo_url = f"https://http.cat/{query}",
    )
    ]
    await update.inline_query.answer(results)

if __name__ == '__main__':
    application = ApplicationBuilder().token(telegramToken).build()
    cat_handler = MessageHandler(filters.TEXT & (~filters.COMMAND) & filters.Regex(r'(^[1-5]\d{2}$)'), cat)
    inline_cat_handler = InlineQueryHandler(inline_cat, r'([1-5]\d{2}$)')
    application.add_handler(cat_handler)
    application.add_handler(inline_cat_handler)
    application.run_polling()