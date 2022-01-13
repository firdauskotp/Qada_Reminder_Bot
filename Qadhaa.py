from pymongo import message
import telegram
from telegram.ext import Updater
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import os
import pymongo
from pymongo import MongoClient
import random, pprint, time
import schedule
from datetime import datetime

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
updater = Updater(token='TOKEN', use_context=True)
client = pymongo.MongoClient("mongodb+srv://<username>:<password>@cluster0.lsslc.mongodb.net/<database>?retryWrites=true&w=majority")

db = client["userDB"]
col1=db["userC"]
day=0
subuh=0
zohor=0
asar=0
maghrib=0
isyak=0
setStatus=0
# usid=0


def start(update: Update, context: CallbackContext):
    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open("./assets/img/icon.jfif", "rb"), caption="Welcome to the QadaBot, your personal Qadha'a and Islamic verse reminder bot! Thank you for choosing us. If you don't have an account, please make one by using the command \
/register. If you have an account, please login using the command /login. If you want to view all the commands, please use the command /help. \n\n PLEASE NOTE THAT IN THIS VERSION, THE BOT USES ASIA/SINGAPORE TIMEZONE")

def remove(update: Update, context: CallbackContext) -> None:

    try:
        getting_status = col1.find({"_id":update.effective_chat.id})
        for getting_id in getting_status:
            setStatus = getting_id["set_status"]
        if setStatus ==1:
            keyboard = [
                [
                    InlineKeyboardButton("Fajr/Subuh", callback_data='7'),
                    InlineKeyboardButton("Dhuhr/Zohor", callback_data='8'),
                    
                    
                ],
                [
                    InlineKeyboardButton("Asr/Asar", callback_data='9'),
                    InlineKeyboardButton("Maghrib", callback_data='10'),
                ],
                [InlineKeyboardButton("Isha/Isyak", callback_data='11'),],
                [InlineKeyboardButton("Back", callback_data='12')],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            update.message.reply_text('Which Prayer Time You Had Replaced?', reply_markup=reply_markup)
        else:
            context.bot.sendMessage(chat_id=update.effective_chat.id, text="Please login to use this function. Use the /help command for more details")
    except:
        context.bot.sendMessage(chat_id=update.effective_chat.id, text="Please login to use this function. Use the /help command for more details")

    #if reply_markup ==1:
        #update.message.reply_text('Which Prayer Time You Want To Set A Reminder To Replace', reply_markup="messages updated")

def qadhaa(update: Update, context: CallbackContext) -> None:
    
    try:
        getting_status_insert = col1.find({"_id":update.effective_chat.id})
        for getting_id_insert in getting_status_insert:
            setStatus = getting_id_insert["set_status"]

        if setStatus == 1:
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
        else:
            context.bot.sendMessage(chat_id=update.effective_chat.id, text="Please login to use this function. Use the /help command for more details")
    except:
        context.bot.sendMessage(chat_id=update.effective_chat.id, text="Please login to use this function. Use the /help command for more details")

    #if reply_markup ==1:
        #update.message.reply_text('Which Prayer Time You Want To Set A Reminder To Replace', reply_markup="messages updated")


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    getting_result_from_id = col1.find({"_id":update.effective_chat.id})

    for getting_results in getting_result_from_id:
        subuh = getting_results["Subuh"]
        zohor = getting_results["Zohor"]
        asar = getting_results["Asar"]
        maghrib = getting_results["Maghrib"]
        isyak = getting_results["Isyak"]

    subuh_total = subuh
    zohor_total = zohor
    asar_total = asar
    maghrib_total = maghrib
    isyak_total = isyak

    if query.data == '1': 
        subuh = subuh + 1
        col1.update_one({"_id":update.effective_chat.id},{"$set":{"Subuh":subuh}})
        query.edit_message_text(text=f"Fajr/Subuh replacement increased by 1")
    elif query.data == '2':
        zohor = zohor + 1
        col1.update_one({"_id":update.effective_chat.id},{"$set":{"Zohor":zohor}})
        query.edit_message_text(text=f"Dhuhr/Zohor replacement increased by 1")
    elif query.data == '3':
        asar = asar + 1
        col1.update_one({"_id":update.effective_chat.id},{"$set":{"Asar":asar}})
        query.edit_message_text(text=f"Asr/Asar replacement increased by 1")
    elif query.data == '4':
        maghrib = maghrib + 1
        col1.update_one({"_id":update.effective_chat.id},{"$set":{"Maghrib":maghrib}})
        query.edit_message_text(text=f"Maghrib replacement increased by 1")
    elif query.data == '5':
        isyak = isyak + 1
        col1.update_one({"_id":update.effective_chat.id},{"$set":{"Isyak":isyak}})
        query.edit_message_text(text=f"Isha/Isyak replacement increased by 1")
    elif query.data == '7':
        if subuh==0:
            query.edit_message_text(text=f"Congrats, you have no Qadha'a left for Subuh ^_^")
        else:
            subuh = subuh - 1
            col1.update_one({"_id":update.effective_chat.id},{"$set":{"Subuh":subuh}})
            query.edit_message_text(text=f"Fajr/Subuh replacement decreased by 1")
    elif query.data == '8':
        if zohor==0:
            query.edit_message_text(text=f"Congrats, you have no Qadha'a left for Zohor ^_^")
        else:
            zohor = zohor - 1
            col1.update_one({"_id":update.effective_chat.id},{"$set":{"Zohor":zohor}})
            query.edit_message_text(text=f"Dhuhr/Zohor replacement decreased by 1")
    elif query.data == '9':
        if asar==0:
            query.edit_message_text(text=f"Congrats, you have no Qadha'a left for Asar ^_^")
        else:
            asar = asar - 1
            col1.update_one({"_id":update.effective_chat.id},{"$set":{"Asar":asar}})
            query.edit_message_text(text=f"Asr/Asar replacement decreased by 1")
    elif query.data == '10':
        if maghrib==0:
            query.edit_message_text(text=f"Congrats, you have no Qadha'a left for Maghrib ^_^")
        else:
            maghrib = maghrib - 1
            col1.update_one({"_id":update.effective_chat.id},{"$set":{"Maghrib":maghrib}})
            query.edit_message_text(text=f"Maghrib replacement decreased by 1")
    elif query.data == '11':
        if isyak==0:
            query.edit_message_text(text=f"Congrats, you have no Qadha'a left for Isyak ^_^")
        else:
            isyak = isyak - 1
            col1.update_one({"_id":update.effective_chat.id},{"$set":{"Isyak":isyak}})
            query.edit_message_text(text=f"Isha/Isyak replacement decreased by 1")
    else:
        query.edit_message_text(text=f"TOTAL REPLACEMENT:\nFajr/Subuh: " + str(subuh_total) +"\nDhuhr/Zohor: "+ str(zohor_total) +"\nAsr/Asar: "+ str(asar_total) +"\nMaghrib: "+ str(maghrib_total) +"\nIsha/Isyak: "+ str(isyak_total))
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
            post_user={"_id":update.effective_chat.id,"name":username,"set_status":0,"Subuh":0,"Zohor":0,"Asar":0,"Maghrib":0,"Isyak":0, "Quotes":0, "Days":0}
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
            col1.update_one({"_id":update.effective_chat.id},{"$set":{"set_status": 1}})
            context.bot.sendMessage(chat_id=update.effective_chat.id, text="Login Successful!")
        else:
            context.bot.sendMessage(chat_id=update.effective_chat.id, text="This username is not registered! Please review the name or register a new username using /reg followed by your username")

def logout(update: Update, context: CallbackContext):
    try:
        getting_status_logout = col1.find({"_id":update.effective_chat.id})
        for getting_id_logout in getting_status_logout:
            setStatus = getting_id_logout["set_status"]

        if setStatus == 1:
            col1.update_one({"_id":update.effective_chat.id},{"$set":{"set_status": 0}})
            context.bot.sendMessage(chat_id=update.effective_chat.id, text="Logout Successful!")
        else:
            context.bot.sendMessage(chat_id=update.effective_chat.id, text="Please login to use this function. Use the /help command for more details")
    except:
        context.bot.sendMessage(chat_id=update.effective_chat.id, text="Please login to use this function. Use the /help command for more details")

def fallback(update:Update, context: CallbackContext):
    context.bot.sendMessage(chat_id=update.effective_chat.id, text="Error, command not found. Please use /help for the available commands")

def total(update:Update, context: CallbackContext):

    get_status_total = col1.find({"_id":update.effective_chat.id})
    for getting_id_total in get_status_total:
        setStatus = getting_id_total["set_status"]

    if setStatus == 1:
        getting_result_from_id = col1.find({"_id":update.effective_chat.id})

        for getting_results in getting_result_from_id:
            subuh_all = getting_results["Subuh"]
            zohor_all = getting_results["Zohor"]
            asar_all = getting_results["Asar"]
            maghrib_all = getting_results["Maghrib"]
            isyak_all = getting_results["Isyak"]

        if subuh_all + zohor_all + asar_all + maghrib_all + isyak_all == 0:
            context.bot.sendMessage(chat_id=update.effective_chat.id, text="Congratulations, you have no prayer to replace! :D")
        else:
            context.bot.sendMessage(chat_id=update.effective_chat.id, text="TOTAL REPLACEMENT:\nFajr/Subuh: " + str(subuh_all) +"\nDhuhr/Zohor: "+ str(zohor_all) +"\nAsr/Asar: "+ str(asar_all) +"\nMaghrib: "+ str(maghrib_all) +"\nIsha/Isyak: "+ str(isyak_all))

    else:
        context.bot.sendMessage(chat_id=update.effective_chat.id, text="Please login to use this function. Use the /help button for more details")

# def offquotes(update:Update, context:CallbackContext):
#     col1.update_one({"_id":update.effective_chat.id},{"$set":{"Quotes": 0}})
#     global usid
#     usid = 0
#     context.bot.sendMessages(chat_id= update.effective_chat.id, text="Quotes turned off, to turn them on again, use the command /onquotes")

def onquotes(update:Update, context:CallbackContext):
    col1.update_one({"_id":update.effective_chat.id},{"$set":{"Quotes": 1}})
    # context.bot.sendMessages(chat_id= update.effective_chat.id, text="Quotes turned on, to turn them off again, use the command /offquotes")

    quotes = ["./assets/img/islamic_quotes/islamic_quotes_1.jpg","./assets/img/islamic_quotes/islamic_quotes_2.jpg","./assets/img/islamic_quotes/islamic_quotes_3.jpg"]
    dua = ["./assets/img/dua/dua_1.jpg","./assets/img/dua/dua_2.jpg","./assets/img/dua/dua_3.jpg","./assets/img/dua/dua_4.jpg","./assets/img/dua/dua_5.jpg"]



    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open(random.choice(quotes),"rb"), caption="Here is an Islamic Quote :)")
    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open(random.choice(dua),"rb"), caption="And here is a beautiful Dua' as well :D")

def extreme_reminder(update:Update, context:CallbackContext):
    grave = ["./assets/img/grave/grave1.jfif","./assets/img/grave/grave2.jfif","./assets/img/grave/grave3.jfif","./assets/img/grave/grave4.jfif"]
    context.bot.sendPhoto(chat_id=update.effective_chat.id, photo=open(random.choice(grave),"rb"), caption="A reminder to replace prayeres you haven't replaced yet")


def help(update:Update, context: CallbackContext):
    context.bot.sendMessage(chat_id=update.effective_chat.id, text="PLEASE NOTE THAT IN THIS VERSION, THE BOT USES ASIA/SINGAPORE TIMEZONE \n \n Thank you for using our bot, we hope you will benefit from it! Here are the available commands \
        \n \n DON'T NEED AN ACCOUNT \n /help = bring up this help message section \n /reg abc = To register your username. Please substitute abc with your desired username. NOTE THAT ONLY ONE USER CAN REGISTER ON ONE ACCOUNT AND YOU CANNOT USE A DUPLICATE USERNAME \
        \n /login abc = To login with your username. Please substitute abc with your username  \n /onquotes = To send Dua' and Islamic quotes \n \n NEED AN ACCOUNT \n /qadhaa = To add the prayer times that is missed. If back is pressed, the total prayer times needed to be replaced is shown \
        \n /remove = To remove a prayer replacement. If back is pressed, the total prayer times needed to be replaced is shown \n /logout = To logout your account \n /total = Shows the total prayer replacements \n /er = An extreme reminder of why we should replace our prayers [TO BE AUTOMATIC IN A FUTURE VERSION]")
start_handler = CommandHandler('start',start)
dispatcher = updater.dispatcher
dispatcher.add_handler(start_handler)

updater.dispatcher.add_handler(CommandHandler('qadhaa', qadhaa))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
updater.dispatcher.add_handler(CommandHandler('remove', remove))
updater.dispatcher.add_handler(CommandHandler('reg', register))
updater.dispatcher.add_handler(CommandHandler('login', login))
updater.dispatcher.add_handler(CommandHandler('logout', logout))
updater.dispatcher.add_handler(CommandHandler('total', total))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('onquotes', onquotes))
updater.dispatcher.add_handler(CommandHandler('er', extreme_reminder))
# updater.dispatcher.add_handler(CommandHandler('offquotes', offquotes))

# updater.dispatcher.add_error_handler(fallback)

now=datetime.now()
current_time = now.strftime("%H:%M")
print(current_time)


checking = {
    'start':start,
    'qadhaa':qadhaa,
    'reg':register,
    'login':login,
    'remove':remove,
    'logout':logout,
    'help':help,
    'total':total,
    'onquotes':onquotes
}


updater.start_polling()
