import telebot
from telebot import types



class User:
    def __init__(self, user):
        self.id = user.id
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.language = None
        self.currencies = None
        self.chat_id = None

########------MARKUPS------##########

#choose a language inline markup
def make_language_markup():
    rus_button = types.InlineKeyboardButton(text = 'RUS', callback_data = 'rus')
    eng_button = types.InlineKeyboardButton(text = 'ENG', callback_data = 'eng')
    language_markup = types.InlineKeyboardMarkup()
    language_markup.add(*[rus_button, eng_button])
    return language_markup

#start keyboard markup
def make_startup_markup():
    start_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_markup.add('Мои криптовалюты')
    start_markup.add('О боте')
    start_markup.add('Помощь/Отзывы')
    return start_markup

#Agreement markup
def make_agreement_rus_markup():
    agreement_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    agreement_markup.add("Принимаю")
    return agreement_markup

def make_agreement_eng_markup():
    agreement_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    agreement_markup.add("Accept")
    return agreement_markup

def make_next_rus_markup():
    next_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    next_markup.add('Далее')
    return next_markup

def make_next_eng_markup():
    next_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    next_markup.add('Next')
    return next_markup
