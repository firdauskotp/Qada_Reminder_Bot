from telegram.ext import Updater
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import os
import pymongo
from pymongo import MongoClient

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
updater = Updater(token='', use_context=True)

db = client["userDB"]
col1=db["userC"]
day=0
subuh=0
zohor=0
asar=0
maghrib=0
isyak=0
setStatus=0


def start(update: Update, context: CallbackContext):
    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2NlXqYdo_6To5nE0KZ0_3J_I0YKuL17ULCg&usqp=CAU", caption="Welcome to the QadaBot, your personal Qadha'a and Islamic verse reminder bot! Thank you for choosing us. If you don't have an account, please make one by using the command \
/register. If you have an account, please login using the command /login. If you want to view all the commands, please use the command /help.")

def qadhaa(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("Fajr/Subuh", callback_data='1'),
            InlineKeyboardButton("Dhuhr/Zohor", callback_data='2'),
            
            
        ],
        [
            InlineKeyboardButton("Asr/Asar", callback_data='3'),
            InlineKeyboardButton("Maghrib", callback_data='4'),
         ],
        [InlineKeyboardButton("Isha/Isyak", callback_data='5'),],
        [InlineKeyboardButton("Back", callback_data='6')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Which Prayer Time You Want To Set A Reminder To Replace', reply_markup=reply_markup)

    #if reply_markup ==1:
        #update.message.reply_text('Which Prayer Time You Want To Set A Reminder To Replace', reply_markup="messages updated")


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    if query.data == '1':
        query.edit_message_text(text=f"Fajr/Subuh replacement increased by 1")
    elif query.data == '2':
        query.edit_message_text(text=f"Dhuhr/Zohor replacement increased by 1")
    elif query.data == '3':
        query.edit_message_text(text=f"Asr/Asar replacement increased by 1")
    elif query.data == '4':
        query.edit_message_text(text=f"Maghrib replacement increased by 1")
    elif query.data == '5':
        query.edit_message_text(text=f"Isha/Isyak replacement increased by 1")
    else:
        query.edit_message_text(text=f"TOTAL REPLACEMENT:\nFajr/Subuh:\nDhuhr/Zohor:\nAsr/Asar:\nMaghtib:\nIsha/Isyak:")

    #query.edit_message_text(text=f"Selected option: {query.data}")

start_handler = CommandHandler('start',start)
dispatcher = updater.dispatcher
dispatcher.add_handler(start_handler)

updater.dispatcher.add_handler(CommandHandler('qadhaa', qadhaa))
updater.dispatcher.add_handler(CallbackQueryHandler(button))



updater.start_polling()


# context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open("./startImage.jpg", "rb"), caption="Welcome to the QadaBot, your personal Qadha'a and Islamic verse reminder bot! Thank you for choosing us. If you don't have an account, please make one by using the command \
#/register. If you have an account, please login using the command /login. If you want to view all the commands, please use the command /help.")
