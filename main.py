import logging
from telegram import InlineQueryResultPhoto, Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, InlineQueryHandler
from helper import codeIsValid, randomCode, codeOptions
from telegramToken import telegramToken

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    codeNumber = update.message.text
    if (codeIsValid(codeNumber)):
        await update.message.reply_photo(f"https://http.cat/{codeNumber}")
        print(f"Kitty {codeNumber} sent to @{update.message.from_user.username}")
    else:
       await update.message.reply_text(text="This code does not exist. Here's a random one instead:")
       await update.message.reply_photo(f"https://http.cat/{randomCode()}")
       print(f"Random kitty sent @{update.message.from_user.username}")
                

async def inline_cat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = []
    for option in codeOptions(query):
        results.append(
            InlineQueryResultPhoto(
            id = option,
            thumbnail_url = f"https://http.cat/{option}",
            photo_url = f"https://http.cat/{option}",
            )
        )
        
    await update.inline_query.answer(results)
    print(f'Inline kitty called by @{update.inline_query.from_user.username}')

if __name__ == '__main__':
    application = ApplicationBuilder().token(telegramToken).build()
    cat_handler = MessageHandler(filters.TEXT & (~filters.COMMAND) & filters.Regex(r'(^[1-5]\d{2}$)'), cat)
    inline_cat_handler = InlineQueryHandler(inline_cat, r'([1-5]\d\d?$)')
    application.add_handler(cat_handler)
    application.add_handler(inline_cat_handler)
    application.run_polling()