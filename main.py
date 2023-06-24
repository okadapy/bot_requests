from telebot import TeleBot
from telebot.types import Message
import settings
from settings import *
from botutil import *

app = TeleBot(TOKEN)
init_db()


def suggest(message: Message) -> None:
    if message.photo is None or message.caption is None:
        return

    photo = message.photo[-1].file_id
    caption = message.caption.lower().split("\n")
    if "фандом:" not in caption[0] or "персонаж:" not in caption[-1]:
        app.reply_to(message, "Заполните новость СТРОГО по форме!")
        app.register_next_step_handler(message, suggest)

    fandom = caption[0].replace("фандом:", "")
    character = caption[-1].replace("персонаж:", "")
    suggestion = Suggestion(photo, fandom, character, getuid(message.from_user.id))
    suggestion.write()


@app.message_handler(commands=["send"])
def send_to_post(message: Message):
    if if_red(message.from_user.id):
        app.reply_to(
            message,
            "Отлично! Пришлите ваш пост. ОБЯЗАТЕЛЬНО уместите его в описании картинки",
        )
        app.register_next_step_handler(message, send_to_post_2)


def send_to_post_2(message):
    caption = message.caption.replace("/send", "")
    app.send_photo(
        settings.POSTS_CHAT, photo=message.photo[-1].file_id, caption=caption
    )


@app.message_handler(commands=["ok"])
def approve(message):
    if message.from_user.id in SUPER_USERS:
        id = message.text.split()[-1]
        notify(Notify.RED_APPROVED, id)
        user = app.get_chat_member(id, id)
        reg(id, user.user.username)


@app.message_handler(commands=["no"])
def deny(message):
    if message.from_user.id in SUPER_USERS:
        id = message.text.split()[-1]
        notify(Notify.RED_DECLINED, id)


@app.message_handler(commands=["start", "предложить"])
def start(message: Message) -> None:
    """Функция для обработки комманд start и пердложить"""
    app.reply_to(
        message,
        "Привет-привет!\n"
        "Для того что бы предложить новость вам нужно прислать фото косплея с подписью формата:\n"
        "*Фандом:* _название_,\n"
        "*Персонаж:* _имя_\n"
        "Удачи!\n\n\n*О БАГАХ И ПРЕДЛОЖЕНИЯХ СООБЩАТЬ*: @idoubtmymentalhealth",
        parse_mode="Markdown",
    )
    create_user(message.from_user.username, message.from_user.id)
    app.register_next_step_handler(message, suggest)


@app.message_handler(commands=["reg"])
def register(message):
    create_user(message.from_user.username, message.from_user.id)
    app.reply_to(
        message,
        f"Ваша заявка отправлена на рассмотрение, @{message.from_user.username}",
    )
    for i in SUPER_USERS:
        app.send_message(
            i,
            text=f"@{message.from_user.username} отправил заявку на авторизацию\n"
            f"Для завершения регистрации введите /ok {message.from_user.id}\n"
            f"Для отклонения: /no {message.from_user.id}",
        )


@app.message_handler(commands=["new"])
def new_post(message: Message) -> None:
    if if_red(message.from_user.id):
        post = get_rnd_post()
        app.send_photo(
            message.from_user.id,
            photo=post[2],
            caption=f"{post[3]}\n{post[4]}\n\nЕсли вы готовы разобрать данный косплей ответьте ДА, иначе - НЕТ",
        )
        app.register_next_step_handler(message, take_post, post[1], post[0])


def take_post(message, tg_id, post_id):
    if "да" in message.text.lower():
        notify(Notify.POST_TAKEN, tg_id)
        set_taken(message.from_user.id, post_id)
        return
    app.reply_to(message, "Жаль!")


def notify(status, tg_id):
    match status:
        case Notify.POST_TAKEN:
            app.send_message(get_usr(tg_id), "Ваш пост приняли на редакцию!")
        case Notify.RED_APPROVED:
            app.send_message(tg_id, "Вы были назначены редактором!")
        case Notify.RED_DECLINED:
            app.send_message(tg_id, "Вам отказали в регистрации!")


app.infinity_polling()
