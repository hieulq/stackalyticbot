#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A telegram bot that manages an alarm clock based on crontab

@author Guy Sheffer (GuySoft) <guysoft at gmail dot com>
"""
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from emoji import emojize
import logging
import os
from bot.utils import stackquery


class Bot:
    def __init__(self, tele_token):

        self.selected_alarm_type = ""
        self.selected_continent = ""
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)

        self.updater = Updater(token=tele_token)
        self.dispatcher = self.updater.dispatcher
        start_handler = CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        self.ALARM_TYPE, self.ALARM_HOUR = range(2)

        self.TIMEZONE_CONTINENT, self.TIMEZONE_TIME = range(2)

        help_handler = CommandHandler('help', self.help)
        self.dispatcher.add_handler(help_handler)

        report_handler = CommandHandler('report', self.report)
        self.dispatcher.add_handler(report_handler)

        self.dispatcher.add_error_handler(self.error_callback)

        echo_handler = MessageHandler(Filters.text, self.echo)
        self.dispatcher.add_handler(echo_handler)

        return

    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text="I'm an alarm bot bot, please type /help for info")
        return

    def echo(self, bot, update):
        print(update.message.text)
        bot.send_message(chat_id=update.message.chat_id,
                         text=update.message.text)
        return

    def report(self, bot, update):
        print(update.message.text)
        patch, table = stackquery.report()
        bot.send_message(chat_id=update.message.chat_id,
                         text=patch.get_string())
        bot.send_message(chat_id=update.message.chat_id,
                         text=table.get_string())
        return

    def error_callback(self, bot, update, error):
        try:
            raise error
        except Unauthorized as e:
            # remove update.message.chat_id from conversation list
            pass
        except BadRequest:
            # handle malformed requests - read more below!
            pass
        except TimedOut:
            # handle slow connection problems
            pass
        except NetworkError:
            # handle other connection problems
            pass
        except ChatMigrated as e:
            # the chat_id of a group has changed, use e.new_chat_id instead
            pass
        except TelegramError:
            # handle all other telegram related errors
            pass
        return

    def help(self, bot, update):
        icon = emojize(":information_source: ", use_aliases=True)
        text = icon + " The following commands are available:\n"

        commands = [["/new", "Create new alarm"],
                    ["/list", "List alarms, enable/disable and remove alarms"],
                    ["/stop", "Stop all alarms"],
                    ["/timezone",
                     "Set the timezone (only works if sudo requires no password)"],
                    ["/test", "Play an alarm to test"],
                    ["/time", "Print time and timezone on device"],
                    ["/help", "Get this message"]
                    ]

        for command in commands:
            text += command[0] + " " + command[1] + "\n"

        bot.send_message(chat_id=update.message.chat_id, text=text)

    def run(self):
        self.updater.start_polling()
        return


if __name__ == "__main__":
    token = os.getenv('TELEGRAM_TOKEN')

    bot = Bot(token)
    bot.run()
    print("Bot Started")
