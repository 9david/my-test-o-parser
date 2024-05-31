from django.core.management.base import BaseCommand
from testparser import telegram_bot

class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **kwargs):
        telegram_bot.main()