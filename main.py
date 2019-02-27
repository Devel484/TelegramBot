#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Neue Bot Generation mit Multithreading. Dispatcher, Updater und JobQueue laufen in separaten Threads.
# Vom Bot initiierte Aktionen werden über die JobQueue gestartet.
#
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job, JobQueue
import logging
import threading
import time
# Enable loggingpip
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s -%(message)s',level=logging.INFO)
logger = logging.getLogger(__name__)
chat_id = None
updater = None


class EchoBotGen3(threading.Thread):

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)

    def run(self):
        global updater
        # Create the EventHandler and pass it your bot's token.
        #
        # PLEASE GET YOUR OWN TOKEN FROM BOTFATHER!!!
        #
        #
        updater = Updater('')
        job_queue = updater.job_queue
        # Get the dispatcher to register handlers
        dp = updater.dispatcher
        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", start))
        dp.add_handler(CommandHandler("help", helpp))
        # on noncommand i.e message - echo the message on Telegram
        dp.add_handler(MessageHandler(Filters.text, echo))
        # add periodocal job generation
        job_queue.run_repeating(intval, interval=30)
        # log all errorsdp.add_error_handler(error)
        # Start the Bot
        updater.start_polling()
        # Define a few command handlers. These usually take the two arguments bot and
        # update. Error handlers also receive the raised TelegramError object in error.


def start(bot, update):
    global chat_id
    chat_id = update.message.chat_id
    update.message.reply_text('Hi!\nDeine Chat ID ist ' +  str(chat_id))


def helpp(bot, update):
    update.message.reply_text('Help!')


def echo(bot, update):
    update.message.reply_text(update.message.text)


def intval(bot, job):
    global chat_id
    if chat_id:
        bot.send_message(chat_id=chat_id, text="Das ist eine erzeugte Nachricht")


def error(bot, update, error):
    global logger
    logger.warning('Update "%s" caused error "%s"' % (update, error))


if __name__ == '__main__':
    eb = EchoBotGen3()
    eb.start()
# Run the bot until the you presses Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
#    updater.idle()
