from os import getenv
from threading import Thread
from time import sleep

import telebot
from feedparser import parse

from models import db, User, SentMessage

db.connect()
db.create_tables([User, SentMessage])

BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")
if not BOT_TOKEN:
    raise BaseException("Вы не передали токен бота")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message: telebot.types.Message):
    User.create(user_id=message.from_user.id)
    bot.reply_to(message, "Вы успешно подписались на рассылку!")


def parse_feed():
    while True:
        feed = parse("http://web/rss/")
        for article in feed.entries:
            for user in User.select():
                if (
                    SentMessage.select()
                    .where(SentMessage.user == user.user_id, SentMessage.message_id == article.link)
                    .exists()
                ):
                    continue
                print(f"Send article {article.title} to {user.user_id}", flush=True)
                SentMessage.create(user=user.user_id, message_id=article.link)

                text = f"[{article.title}]({article.link})\n\n"
                for paragraph in article.description.split("\n"):
                    text += f"- {paragraph}\n"

                bot.send_message(chat_id=user.user_id, text=text, parse_mode="Markdown", disable_web_page_preview=True)
                sleep(10)
        sleep(600)
        sleep(600)



if __name__ == "__main__":
    Thread(target=parse_feed).start()
    bot.infinity_polling()
