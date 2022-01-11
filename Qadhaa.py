from pymongo import message
import telegram
from telegram.ext import Updater
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import os
import pymongo
from pymongo import MongoClient
import random, pprint, requests

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
updater = Updater(token='5006375684:AAGL9DwGk9DsS1XVU-uwT48K8-VkdpRA0Dw', use_context=True)
client = pymongo.MongoClient("mongodb+srv://fkna:firdausafiqkhaiacap@cluster0.lsslc.mongodb.net/userDB?retryWrites=true&w=majority")

db = client["userDB"]
col1=db["userC"]
day=0
subuh=0
zohor=0
asar=0
maghrib=0
isyak=0
setStatus=0

#lists of pictures
grave = ["./assets/img/grave/grave1.jfif","./assets/img/grave/grave2.jfif","./assets/img/grave/grave3.jfif","./assets/img/grave/grave4.jfif"]
jumpscare = [2,3,4]
Quran_Verse = [1,2,3]

#Reminders
#Al Mulk
#Surah Kahfi
#Quotes

def start(update: Update, context: CallbackContext):
    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open("./assets/img/icon.jfif", "rb"), caption="Welcome to the QadaBot, your personal Qadha'a and Islamic verse reminder bot! Thank you for choosing us. If you don't have an account, please make one by using the command \
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

def register(update: Update, context: CallbackContext):
    
    print (update.message.text)
    entitites = update.message.entities

    for x in entitites:
        print(x)
    command = update.message.text
    l=3
    print(len(command[0+l+1:].strip()))
    if len(command[0+l+1:].strip())==0:
        context.bot.sendMessage(chat_id=update.effective_chat.id, text="Please input a name to register. Example: /reg test")
    else:
        username=command[0+l+1:].strip()
        username_query=col1.find({"name":username})
        id_query=col1.find({"_id":update.effective_chat.id})

        check_register_user=0
        check_register_id=0

        for get_reg_user in username_query:
            check_register_user+=1
        for get_reg_id in id_query:
            check_register_id+=1
        
        if check_register_user==0 and check_register_id==0:
            post_user={"_id":update.effective_chat.id,"name":username,"set_status":0}
            col1.insert_one(post_user)
            context.bot.sendMessage(chat_id=update.effective_chat.id, text="Congratulations, your username is registered!")
        else:
            context.bot.sendMessage(chat_id=update.effective_chat.id, text="Username is taken or there is an account on your current Telegram account! Please use another username")


def login(update: Update, context: CallbackContext):
    entitites = update.message.entities

    for x in entitites:
        print(x)
    command = update.message.text
    l=5
    print(len(command[0+l+1:].strip()))
    if len(command[0+l+1:].strip())==0:
        context.bot.sendMessage(chat_id=update.effective_chat.id, text="Please input a name to login. Example: /login test")
    else:
        username=command[0+l+1:].strip()
        username_query = col1.find({"name":username})
        check_logged_user=0
        for getting_logging_users in username_query:
            check_logged_user+=1
        if check_logged_user>0:
            col1.update_one({"_id":update.effective_chat.id},{"$set":{"set-status": 1}})
            context.bot.sendMessage(chat_id=update.effective_chat.id, text="Login Successful!")
        else:
            context.bot.sendMessage(chat_id=update.effective_chat.id, text="This username is not registered! Please review the name or register a new username using /reg followed by your username")

def logout(update: Update, context: CallbackContext):
    col1.update_one({"_id":update.effective_chat.id},{"$set":{"set-status": 0}})
    context.bot.sendMessage(chat_id=update.effective_chat.id, text="Logout Successful!")
    

def fallback(update:Update, context: CallbackContext):
    context.bot.sendMessage(chat_id=update.effective_chat.id, text="Error, command not found. Please use /help for the available commands")

start_handler = CommandHandler('start',start)
dispatcher = updater.dispatcher
dispatcher.add_handler(start_handler)

updater.dispatcher.add_handler(CommandHandler('qadhaa', qadhaa))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('reg', register))
# updater.dispatcher.add_error_handler(fallback)


checking = {
    'start':start,
    'qadhaa':qadhaa,
    'reg':register
}

print(checking.keys())

updater.start_polling()


# context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open("./startImage.jpg", "rb"), caption="Welcome to the QadaBot, your personal Qadha'a and Islamic verse reminder bot! Thank you for choosing us. If you don't have an account, please make one by using the command \
#/register. If you have an account, please login using the command /login. If you want to view all the commands, please use the command /help.")

#context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open(random.choice(grave),"rb"), caption="test")