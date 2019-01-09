import telebot
from telebot import types
import botan
import TeleConfig
from TeleUtils import *
import time
from random import randint
from multiprocessing import Process
#------------------------DATABASE------------------------
import sqlite3



def create_table():#need to be done onece, creates table
    conn = sqlite3.connect('buffett_bot.db')# connect database
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS subscribers_table (client_chat_id TEXT, client_status REAL, client_tg_name TEXT, client_tg_username TEXT, client_language TEXT, client_bot_id REAL)')
    c.close()
    conn.close()

def add_new_user(client_chat_id, client_tg_name, client_tg_username, client_language, client_bot_id):#uses chat_id
    if client_chat_id not in return_list_of_users(status=0):#check weather we already have this user in database
        conn = sqlite3.connect('buffett_bot.db')# connect database
        c = conn.cursor()
        c.execute("INSERT INTO subscribers_table VALUES(?, ?, ?, ?, ?, ?)",
        (client_chat_id, 0, client_tg_name, client_tg_username, client_language, client_bot_id))
        conn.commit()#save changes
        c.close()
        conn.close()

def change_status(client_chat_id, subscription_length):#changes status of user
    conn = sqlite3.connect('buffett_bot.db')# connect database
    c = conn.cursor()
    c.execute("UPDATE subscribers_table SET client_status = ? WHERE client_chat_id = ?",
    (subscription_length,client_chat_id))
    conn.commit()
    c.close()
    conn.close()

def return_list_of_users(status=1):#returns the list of users who signed agreement and has status = 1
    conn = sqlite3.connect('buffett_bot.db')# connect database
    users_list = []
    c = conn.cursor()
    if status == 1:
        c.execute('SELECT client_chat_id FROM subscribers_table WHERE client_status=1.0')
        for i in c.fetchall():
            users_list.append(int(str(i)[2:-3]))
    elif status == 0:
        c.execute('SELECT client_chat_id FROM subscribers_table')
        for i in c.fetchall():
            users_list.append(int(str(i)[2:-3]))

    c.close()
    conn.close()
    return users_list

create_table()#create tble of all our users
#-------------------------------------------------------

bot = telebot.TeleBot(TeleConfig.token)#configure bot

CurrentLine = None
last_announcement = None
last_direct_msg = None
last_direct_chat_id = None
keyboard_hider = types.ReplyKeyboardRemove()

number_of_accepts = 0
number_of_start = 0
number_of_next = 0
number_of_language = 0



def send_message_to_all_our_users(msg,status):#sends msg to all our users
    for i in return_list_of_users(status):
        bot.send_message(
        i,
        text = eval(msg),
        parse_mode = 'Markdown')


def polling():
    bot.polling(none_stop=True)

def main():
    try:
        print("1")
        if __name__ == '__main__':
            Process(target=start_streaming).start()
            bot.polling(none_stop=True)
            #Process(target=start_streaming).start()
    except BaseException as e:
        print(str(e))
        time.sleep(900)
        main()


def start_streaming():
    global CurrentLine
    if number_of_accepts < 2:
        while True:
            send_announcement()#if there is any announcement in announcement_check.txt then it will be sent to all the user and continue it's work
            fileHandle = open('./data_v2.txt',"r")#open archive file with all tweets
            line_list = fileHandle.readlines()#list of data_v2.txt lines
            if line_list[-1] != CurrentLine: #if  last line is not the same as the current line then it's a new tweet
                #start_markup = make_startup_markup()
                send_message_to_all_our_users(line_list[-1],status=1) # send a new tweet
                CurrentLine = line_list[-1]# refresh current line
            fileHandle.close()

def disclaimer_agree(chat_id, user_language):
    if user_language == 'rus':
        #botan.track(TeleConfig.botan_key, chat_id, None, 'RUS language')
        #disclaimer text and markup 'I agree'
        msg = bot.send_message(
        chat_id,
        text= 'Для того чтобы воспользоваться услугами данного бота примите "Отказ от ответственности": ' + TeleConfig.disclaimer_rus,
        parse_mode = 'Markdown',
        reply_markup = make_agreement_rus_markup())
        bot.register_next_step_handler(msg, agreement_check_and_streaming_start)
        #then we redirect the answer to agreement_check_and_streaming_start function
    elif user_language == 'eng':
        #botan.track(TeleConfig.botan_key, chat_id, None, 'ENG language')
        #disclaimer text and markup 'I agree'
        msg = bot.send_message(
        chat_id,
        text= 'In order to use this bot, please, accept the following Disclaimer: ' + TeleConfig.disclaimer_eng,
        parse_mode = 'Markdown',
        reply_markup = make_agreement_eng_markup())
        bot.register_next_step_handler(msg, agreement_check_and_streaming_start)
        #then we redirect the answer to agreement_check_and_streaming_start function

def agreement_check_and_streaming_start(message):
    global number_of_accepts
    if message.text == "Принимаю":
        #get and save needed info to database
        user_tg_id = message.from_user.username
        user_tg_language = message.from_user.language_code
        name = str(message.chat.first_name + " " + message.chat.last_name)
        client_bot_id = randint(1000000, 9999999)
        add_new_user(str(chat_id), str(name), str(user_tg_id), str(user_tg_language), client_bot_id)

        number_of_accepts += 1
        botan.track(TeleConfig.botan_key, message.chat.id, message, 'accept')
        bot.send_message(
        chat_id,
        text = "Бот начнет работу после оформления подписки.\nЦены на подписку:\n1 месяц - 1500 рублей\n3 месяца - 3600 рублей\n6 месяцев - 6000 рублей\nДля того чтобы оформить подписку перешлите сумму для нужной подписки на карту\n4276 3800 6737 1760\nс единственным комментарием: *{!s}*. После этого ваш бот будет активирован в течении 8 часов.".format(client_bot_id),
        parse_mode = 'Markdown', reply_markup = keyboard_hider)
        time.sleep(1)
    elif message.text == "Accept":
        #get and save needed info to database
        user_tg_id = message.from_user.username
        user_tg_language = message.from_user.language_code
        name = str(message.chat.first_name + " " + message.chat.last_name)
        client_bot_id = randint(1000000, 9999999)
        add_new_user(str(chat_id), str(name), str(user_tg_id), str(user_tg_language), client_bot_id)

        number_of_accepts += 1
        botan.track(TeleConfig.botan_key, message.chat.id, message, 'accept')
        bot.send_message(chat_id,
        text = "The bot will start working after you subscribe. Subscription price:\n1 month - 25$\n3 months - 60$\n6 months - 100$\nIn order to subscribe, send the amount for the required subscription to the card\n4276 3800 6737 1760\nwith the only comment: *{!s}*. After that, your bot will be activated within 8 hours.".format(client_bot_id),
        parse_mode = 'Markdown',reply_markup = keyboard_hider)
        time.sleep(1)



@bot.message_handler(commands=['start'])# starting a bot
def send_welcome(msg):
    global number_of_start
    number_of_start += 1
    if number_of_start < 2 and msg.chat.id not in return_list_of_users(status=0):
        botan.track(TeleConfig.botan_key, msg.chat.id, msg, 'Start')
        global chat_id
        chat_id = msg.chat.id
        global user_first_name
        user_first_name = msg.chat.first_name
        bot.send_message(msg.chat.id, 'Select a language:', reply_markup=make_language_markup())#this is an inline buttons of language, that means that the answer goes to callback handler


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global number_of_language
    global user_language
    user_language = call.data# on this step we've got users' language that we wanted to know in "command = start" handler(privious one)
    if call.data == "rus" and number_of_language < 1:
        number_of_language += 1
        #Welcome and bot description
        message = bot.send_message(
        chat_id,
        text= "Здравствуйте, *{!s}*!\nДанный бот следит за твиттер-аккаунтами различных криптовалют и будет присылать вам только те новости, в которых есть определенные ключевые слова, такие как introducing, soon, announcement и другие. Часто на таких новостях происходит значительное колебание валюты, на чем можно заработать. Вы будете информированы немедленно при появлении важных обновлений в Топ-75 криптовалют.".format(user_first_name),
        parse_mode = 'Markdown', reply_markup = make_next_rus_markup())
        bot.register_next_step_handler(message, next_check)
    elif call.data == "eng" and number_of_language < 1:
        number_of_language += 1
        message = bot.send_message(
        chat_id,
        text= 'Hello, *{!s}*!\nThis bot follows Twitter accounts of various crypto currencies and will send you only news contain certain keywords such as "introducing", "soon", "announcement" and others. Often currencies fluctuate with such news, on which one can earn. You will be informed immediately when important updates appear in the Top 75 crypto currencies.'.format(user_first_name),
        parse_mode = 'Markdown', reply_markup = make_next_eng_markup())
        bot.register_next_step_handler(message, next_check)
    #After we gave a brief description we start the preprocess of disclaimer agree



def next_check(message):
    global number_of_next
    if message.text == "Далее" or message.text == "Next" and number_of_next < 1:
        number_of_next += 1
        time.sleep(1)
        disclaimer_agree(chat_id, user_language)

##########-----ANNOUNCEMENTS-----############
def send_announcement():
    try:
        f = open("announcement_check.txt", 'r')
    except BaseException:
        time.sleep(1)
        f = open("announcement_check.txt", 'r')
    global last_announcement
    announcement_msg = f.readline()
    if announcement_msg != "" and announcement_msg != None and announcement_msg != last_announcement:#checks wheather there is any announcement if there is, bot sends it to all users
        send_message_to_all_our_users(announcement_msg, status=0)
        last_announcement = announcement_msg
    f.close()

main()
