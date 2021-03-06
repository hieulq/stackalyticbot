"""Get report from Stackalytics
/cureport - Get report from Stackalytics

Usage:

- Chat direct with bot and upload config file in json format.

For e.x:
    {
        "company": "Fujitsu",
        "members": [
            "kiennt26",
            "daidv"
        ],
        "review_target": 6969,
        "commit_target": 696
    }
- Type /cureport hour:minute
"""
from datetime import time
import json
import logging

from telegram import ParseMode
import xlsxwriter

from telebot.utils import emojies
from telebot import utils
from telebot.plugins import stackalytics

LOG = logging.getLogger(__name__)


def do_report(bot, job):
    chat_id = job.context['chat_id']
    try:
        config = json.load(open('config.json'))
    except FileNotFoundError:
        msg = 'Config file doesn\'t exist! Type /help stackalytics again to \
               check usage!'
        utils.handle_error(LOG, bot, chat_id, msg)
        return
    except json.decoder.JSONDecodeError:
        msg = 'Wrong format! Type /help stackalytics again to \
              check right format!'
        utils.handle_error(LOG, bot, chat_id, msg)
        return

    bot.send_message(chat_id=chat_id,
                     text=emojies.no_speak +
                          'Report time, please wait for seconds...')

    text = '{} *Report:*\n' . format(emojies.point_right)
    targets = (int(config['review_target']), int(config['commit_target']))
    report_file = 'FVL_UC_Contribution_Summarization.xlsx'
    workbook = xlsxwriter.Workbook(report_file)
    num_members = len(config['members'])
    team_stats_patches = 0
    team_stats_commits = 0
    team_stats_reviews = 0
    worksheet = workbook.add_worksheet()

    for index, name in enumerate(config['members']):
        results = stackalytics.query(bot, chat_id,
                                     user_id=config['members'][name],
                                     company=config['company'])
        if not results:
            continue

        patches, commits, reviews = results
        team_stats_commits += commits
        team_stats_patches += patches
        team_stats_reviews += reviews

        text = stackalytics.get_report(workbook, worksheet, name,
                                       (reviews, commits), targets,
                                       num_members, index, text)

    text = stackalytics.get_report(workbook, worksheet, 'Team',
                                   (team_stats_reviews, team_stats_commits),
                                   targets, num_members, 0, text, summary=True)

    workbook.close()

    bot.send_message(chat_id=chat_id,
                     text=text,
                     parse_mode=ParseMode.MARKDOWN)

    bot.send_document(chat_id=chat_id,
                      document=open(report_file, 'rb'),
                      caption='Report')
    return


def handle(bot, update, args, job_queue, chat_data):
    """Report at xx:xx everyday"""
    chat_id = update.message.chat_id
    context = {}

    try:
        hour, minute = map(int, args[0].split(':'))
        context['chat_id'] = chat_id

        # Remove the previous set report
        if 'job' in chat_data:
            job = chat_data['job']
            job.schedule_removal()
            del chat_data['job']

        job = job_queue.run_daily(do_report,
                                  days=(0, 1, 2, 3, 4), # Run MON->FRI
                                  time=time(hour=hour, minute=minute),
                                  context=context)
        chat_data['job'] = job

        update.message.reply_text('Timer successfully set!')

    except(IndexError, ValueError):
        update.message.reply_text('Usage: /cureport hour:minute.')
