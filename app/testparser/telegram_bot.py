import asyncio
from asgiref.sync import sync_to_async
import logging
from datetime import timedelta
import os

from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackContext,
    MessageHandler,
    filters)

from django.db.models import Max
from core.models import Product

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
    )
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def telegram_notifications(num):
    async def send_notification(num):
        bot = Bot(BOT_TOKEN)
        async with bot:
            await bot.send_message(
                chat_id=CHAT_ID,
                text=f'Задача на парсинг товаров с сайта Ozon завершена. '
                     f'Сохранено: {num} товаров.'
            )
    asyncio.run(send_notification(num))


async def greetings(chat_id: int, user_name: str):
    bot = Bot(token=BOT_TOKEN)
    async with bot:
        await bot.send_message(
            chat_id=chat_id,
            text=f'Привет, {user_name}! На данный момент я могу выполнять '
                 f'две функции: оповещать о сохранненых товарах и выводить '
                 f'их последний список, который вы отпарсили!'
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    user_name = update.message.from_user.first_name

    logging.info(f"Received message from {user_name} in chat {chat_id}")

    await greetings(chat_id, user_name)


async def spisok_tovarov(update: Update, context: CallbackContext) -> None:
    latest_datetime = await sync_to_async(
        lambda: Product.objects.aggregate(
            latest_datetime=Max('created_at'))['latest_datetime']
        )()

    start_datetime = latest_datetime - timedelta(seconds=30)

    latest_records = await sync_to_async(
        lambda: list(Product.objects.filter(
            created_at__range=(start_datetime, latest_datetime)))
        )()

    for query in latest_records:
        message = (
            f'ID - {query.id}\n'
            f'Name - {query.name}\n'
            f'URL - {query.description}'
        )

        await update.message.reply_text(message)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    app.add_handler(CommandHandler("spisok_tovarov", spisok_tovarov))
    app.add_handler(message_handler)
    app.run_polling()


if __name__ == '__main__':
    main()

