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
        self.updater = Updater(token)
        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", self.start))
        schedule.every(period).minutes.do(self._fetch)
        self.updater.start_polling()
        while True:
            schedule.run_pending()
            time.sleep(1)

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
                self.updater.bot.send_message(id, text=res)

    def _fetch(self):
        self.send_result(self.get_update())

    def get_update(self):
        return "update"
