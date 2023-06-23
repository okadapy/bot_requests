from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
from flask import Flask, render_template, request
import flask_sqlalchemy
from threading import Thread

TOKEN = "5693917053:AAE1Dvrni97ENKfHe9DgaMRn16kLAIoJhUs"
bot = TeleBot(TOKEN)
app = Flask(__name__)


class Requested(object):
    pictures = list()
    fandom = str()
    character = str()
    text = ""

    def __init__(self, author_id: int, author_name: str):
        self.author = (author_id, author_name)

    def add_fandom(self, fandom: str):
        self.fandom = fandom.strip()

    def set_char(self, charname: str):
        self.character = charname.strip()

    def add_text(self, text: str):
        self.text = text.strip()

    def add_pic(self, message: Message):
        photo = message.photo[-1].file_id

    def start_markup(self):
        buttons = [KeyboardButton("Фото") if self.pictures.__len__() < 3 else None,
                   KeyboardButton("Фандом") if self.fandom == "" else None,
                   KeyboardButton("Персонаж") if self.character == "" else None,
                   KeyboardButton("Примечания") if self.text == "" else None]
        return ReplyKeyboardMarkup(resize_keyboard=True).add(*buttons)



def logic_(message: Message, requested: Requested):
    step = message.text.strip().lower()
    match step:
        case "фото":
            bot.reply_to(message, "Отлично, пришлите фотограффию косплея", reply_markup=None)
            bot.register_next_step_handler(message, )
        case "фандом":

        case "персонаж":

        case "примечния"


@bot.message_handler(commands=['start', 'предложить'])
def bot_main(message: Message):
    requested = Requested(message.from_user.id, message.from_user.username)
    bot.send_message(message.from_user.id,
                     "👋 Привет!\nДля того что бы продолжить\nЗаполни все пункты",
                     reply_markup = requested.start_markup())
    bot.register_next_step_handler(message, logic_, requested)



bot.infinity_polling()
