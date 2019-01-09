Preparation:
Before you run the code, you need to make sure you have the next python libraries:
nltk
tweepy
pytelegrambotapi(this is the pip name, but in code it's imported as a telebot)

How to run it?
Programs Tbot.py(in charge of sending messages to users in telegram) and parser.py(in charge of parsing twitter accounts) should run simultaniously on one machine.

What is what?
config.py - config file for parser.py (twitter bot)
parser.py - parsing od twitter accounts
data_v2.txt - text file where all tweets with keywords go
TeleConfig.py - config file for Tbot.py (telegram bot)
Tbot.py - telegram bot