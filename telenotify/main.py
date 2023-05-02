import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import schedule
import time

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


class Telenotify:

    def __init__(self, token, period=30):
        self.chat_list = {}
        self.send_pool = []
        self.telegram_bot = TelegramBot(token, self.start)
        self.task_scheduler = TaskScheduler(self._fetch, period)
        self.task_scheduler.run()

    def start(self, update: Update, context: CallbackContext) -> None:
        if update.message.chat_id not in self.chat_list:
            self.chat_list[update.message.chat_id] = update
            update.message.reply_text('Hello {}!'.format(update.effective_chat.first_name))
            self._fetch()
        else:
            update.message.reply_text('Already Started.')

    def send_result(self, res):
        if len(res) > 0:
            logger.info(res)
            for id, _ in self.chat_list.items():
                self.telegram_bot.send_message(id, text=res)

    def _fetch(self):
        self.send_result(self.get_update())

    def get_update(self):
        return "update"


class TelegramBot:

    def __init__(self, token, start_command_handler):
        self.updater = Updater(token)
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", start_command_handler))
        self.updater.start_polling()

    def send_message(self, chat_id, text):
        self.updater.bot.send_message(chat_id, text)


class TaskScheduler:

    def __init__(self, task, period):
        self.task = task
        self.period = period
        schedule.every(self.period).minutes.do(self.task)

    def run(self):
        while True:
            schedule.run_pending()
            time.sleep(1)
