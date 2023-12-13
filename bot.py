from telegram import Bot
from telegram import Update
from telegram import ParseMode
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from telegram.ext import CallbackQueryHandler
from telegram.utils.request import Request
import random
import math
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
import csv, io, datetime
import sys
import io

import table
import json

print ("Begining work...")

onlineUsers = table.getAllData()

channel_chat_id = 000
notifySecret = "<>"

BUTTON_INLINE_ONLINE = "button_inline_online"
BUTTON_INLINE_USERS = "button_inline_users"
BUTTON_INLINE_BACK = "button_inline_back"
BUTTON_INLINE_CANCEL = "button_inline_cancel"
BUTTON_INLINE_KEY = "button_inline_key"
BUTTON_INLINE_PREV = "button_inline_prev"
BUTTON_INLINE_NEXT = "button_inline_next"
BUTTON_INLINE_NOTIFY = "button_inline_notify"
SUBSCRIB_DISABLE = "subscrib_disable"
SUBSCRIB_ENABLE = "subscrib_enable"

startMessage = [
    '<a href="https://cdn.cloudflare.steamstatic.com/steam/apps/691260/capsule_616x353.jpg?t=1647546308">&#8205;</a>Привет!',
    'Бот может показать кто сейчас в игре. \nДелает он это на основе статистики игр за день, то есть каждые 15 минут бот смотрит изменилось ли количество сыграных игр за день у пользователя, и если изменилось то бот считает его онлайн',
    'Так как бот проверяет информацию каждые 15 минут, данные не всегда могут быть актуальные в текущий момент времени'
]

tips = [
    '<a href="https://tradexports.com/wp-content/uploads/2022/09/drink-462776_640.jpg">&#8205;</a>Совет 1:\nПорезал пальчик? Не беда, \nвыпей коллы чтоб ранка поскорее зажила',
    '<a href="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS0EHQ0oQkKvMAWslr9r2DB6ORa17W1f0G_MA&usqp=CAU">&#8205;</a>Совет 2:\nГраната это конечно хорошо, но пробовал ли ты кинуть сразу 2?',
    '<a href="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZu3LmEBUh2xpa5QV4Y3VIX3xg7mZOgf7RAw&usqp=CAU">&#8205;</a>Совет 3:\nТоповый игрок, заметив что по нему стреляют, успевает отстроить Тадж Махал в натуральную величину ',
    '<a href="https://www.google.com/imgres?imgurl=https%3A%2F%2Fstatic.wikia.nocookie.net%2Fpopulation-one-vr%2Fimages%2F8%2F8f%2FKnife_Pop_One.png%2Frevision%2Flatest%3Fcb%3D20210910035409&tbnid=7G6rabMuSEq9YM&vet=12ahUKEwjYq7LI0ur9AhUYsioKHTg8AI4QMygHegUIARCtAQ..i&imgrefurl=https%3A%2F%2Fpopulation-one-vr.fandom.com%2Fwiki%2FKnife&docid=JX-zEKrkt7qKMM&w=500&h=281&q=population%20one%20ciberblade&ved=2ahUKEwjYq7LI0ur9AhUYsioKHTg8AI4QMygHegUIARCtAQ">&#8205;</a>Совет 4:\nСтрелять лучше в голову, меча это тоже касается (75 по голове, 25 по туловищу) теперь ты знаешь почему тебя так быстро нарезают на кусочки ',
    '<a href="https://vrgamefaqs.com/wp-content/uploads/2021/12/populationonemenu6.jpg">&#8205;</a>Совет 5:\nТунельное зрение можно отключить. В отличии от кривых рук',
    '<a href="https://uploadvr.com/wp-content/uploads/2021/02/LMG-Teaser-scaled.jpg">&#8205;</a>Совет 6:\nЧем больше звезд, тем круче. Главное не путать с ГТА',
    '<a href="https://techtipsvr.com/wp-content/uploads/2020/11/defib-1024x605.jpeg">&#8205;</a>Совет 7:\nНачинай заряжать заранее, чтобы твой тимейт ожил сразу как долетит до тебя. так он сможет быстрее снова умереть',
    '<a href="https://uploadvr.com/wp-content/uploads/2021/02/Melee-Knife-Teaser-scaled.jpg">&#8205;</a>Совет 8:\nПрикрывай тылы\nБлаго в этой игре слышно всех и всегда, но для этого нужно слушать',
    '<a href="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRjxjLCYKl3bzpZh2rSJUnxKS-8-nO6OBCJjw&usqp=CAU">&#8205;</a>Совет 9:\nНе ленись поучиться стрелять в тире. Основные навыки которые ты должен освоить:\n-Стрельба одной рукой\n-Стрельба без рук\n-Телекинез'

]

inviteMassage = '<a href="http://www.populationonevr.com/images/fistbump.jpg">&#8205;</a>Напиши под сообщением свой ник в игре, чтобы информация о тебе появилась в боте. Так же, можешь указать вместе с ником и свой инвайт ключ\nДля этого отправь сообщение вида:\n\nНик в игре (обязательно)\nИнвайт ключ (не обязательно)\n\nПример:\nPopvanMaster\nXXX-12FT-POFU-7'

moderMassage = '<a href="https://celes.club/uploads/posts/2022-10/1666816058_2-celes-club-p-dovolnii-kotik-pinterest-2.jpg">&#8205;</a>Спасибо\nДанные пройдут модерацию после чего будут добавлены в бот'

notifyMassage = '<a href="https://vr-j.ru/wp-content/uploads/2022/08/Population-One-Duos.jpeg">&#8205;</a><b>Подписка на сообщения об открытии комнаты</b>\n\nЕсли подписка активна, то информация об открытии комнаты, будет появляться в боте в виде сообщений'

#Кнопки под сообщением#
def get_base_inline_keyboard_cancel():
    keyboard = [
        [
            InlineKeyboardButton("Отменить", callback_data=BUTTON_INLINE_CANCEL)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_base_inline_keyboard_start():
    keyboard = [
        [
            InlineKeyboardButton("Кто Онлайн", callback_data=BUTTON_INLINE_ONLINE),
            InlineKeyboardButton("Список всех", callback_data=BUTTON_INLINE_USERS),
        ],
        [
            InlineKeyboardButton("CustomRooms подписка", callback_data=BUTTON_INLINE_NOTIFY),
        ],
        [
            InlineKeyboardButton("Указать свой ник|ключ", callback_data=BUTTON_INLINE_KEY),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_base_inline_keyboard_continue():
    keyboard = [
        [
            InlineKeyboardButton("Кто Онлайн", callback_data=BUTTON_INLINE_ONLINE),
            InlineKeyboardButton("Список всех", callback_data=BUTTON_INLINE_USERS),
        ],
        [
            InlineKeyboardButton("CustomRooms подписка", callback_data=BUTTON_INLINE_NOTIFY),
        ],
        [
            InlineKeyboardButton("Указать свой ник|ключ", callback_data=BUTTON_INLINE_KEY),
        ],
        [
            InlineKeyboardButton("Назад", callback_data=BUTTON_INLINE_BACK)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_base_inline_keyboard_pages():
    keyboard = [
        [
            InlineKeyboardButton("<<", callback_data=BUTTON_INLINE_PREV),
            InlineKeyboardButton(">>", callback_data=BUTTON_INLINE_NEXT),
        ],
        [
            InlineKeyboardButton("Кто Онлайн", callback_data=BUTTON_INLINE_ONLINE),
            InlineKeyboardButton("Список всех", callback_data=BUTTON_INLINE_USERS),
        ],
        [
            InlineKeyboardButton("CustomRooms подписка", callback_data=BUTTON_INLINE_NOTIFY),
        ],
        [
            InlineKeyboardButton("Указать свой ник|ключ", callback_data=BUTTON_INLINE_KEY),
        ],
        [
            InlineKeyboardButton("Назад", callback_data=BUTTON_INLINE_BACK)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def inline_main_submit_disable():
    keyboard = [
        [
            InlineKeyboardButton("Отменить", callback_data=SUBSCRIB_DISABLE)
        ],
        [
            InlineKeyboardButton("Назад", callback_data=BUTTON_INLINE_BACK)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def inline_main_submit_enable():
    keyboard = [
        [
            InlineKeyboardButton("Оформить", callback_data=SUBSCRIB_ENABLE)
        ],
        [
            InlineKeyboardButton("Назад", callback_data=BUTTON_INLINE_BACK)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


#Обработчик ВСЕХ кнопок со ВСЕХ клавиатур#
def keyboard_callback_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    chat_id = update.effective_message.chat_id

    if data == BUTTON_INLINE_ONLINE:
        text = getOnline()
        context.bot.edit_message_text(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.HTML,
            message_id=query.message.message_id,
            reply_markup=get_base_inline_keyboard_continue()
        )
    elif data == BUTTON_INLINE_USERS:
        table.createCount()
        table.setUserPage(chat_id,1)
        text = getAll(1)
        context.bot.edit_message_text(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.HTML,
            message_id=query.message.message_id,
            reply_markup=get_base_inline_keyboard_pages()
        )
    elif data == BUTTON_INLINE_KEY:
        table.createTableAwaiting()
        table.setUser(chat_id)
        table.setSubscrib("true", chat_id)
        context.bot.edit_message_text(
            chat_id=chat_id,
            text= inviteMassage,
            parse_mode=ParseMode.HTML,
            message_id=query.message.message_id,
            reply_markup=get_base_inline_keyboard_cancel()
        )
    elif data == BUTTON_INLINE_BACK:
        text = startMessage
        context.bot.edit_message_text(
            chat_id=chat_id,
            text='\n'.join(text),
            parse_mode=ParseMode.HTML,
            message_id=query.message.message_id,
            reply_markup=get_base_inline_keyboard_start()
        )
    elif data == BUTTON_INLINE_CANCEL:
        table.setSubscrib("false", chat_id)
        text = startMessage
        context.bot.edit_message_text(
            chat_id=chat_id,
            text='\n'.join(text),
            parse_mode=ParseMode.HTML,
            message_id=query.message.message_id,
            reply_markup=get_base_inline_keyboard_start()
        )
    elif data == BUTTON_INLINE_PREV:
        pageNumber = table.getCurrentPage(chat_id)-1 if table.getCurrentPage(chat_id) > 1 else 1
        table.setUserPage(chat_id,pageNumber)
        text = getAll(pageNumber)
        try:
            context.bot.edit_message_text(
                chat_id=chat_id,
                text=text,
                parse_mode=ParseMode.HTML,
                message_id=query.message.message_id,
                reply_markup=get_base_inline_keyboard_pages()
            )
        except BaseException as error:
            print(error)
    elif data == BUTTON_INLINE_NEXT:
        pageNumber = table.getCurrentPage(chat_id)+1 if table.getCurrentPage(chat_id) < math.ceil(len(table.getAllData())/15) else math.ceil(len(table.getAllData())/15)
        table.setUserPage(chat_id,pageNumber)
        text = getAll(pageNumber)
        try:
            context.bot.edit_message_text(
                chat_id=chat_id,
                text=text,
                parse_mode=ParseMode.HTML,
                message_id=query.message.message_id,
                reply_markup=get_base_inline_keyboard_pages()
            )
        except BaseException as error:
            print(error)
    elif data == SUBSCRIB_ENABLE:
        user_id=update.effective_message.chat_id
        table.setSubscribNotify("true", user_id)
        context.bot.answer_callback_query(callback_query_id=query.id, text="Подписка оформлена", show_alert=True)
        context.bot.edit_message_text(
            chat_id=chat_id,
            text=notifyMassage,
            parse_mode=ParseMode.HTML,
            message_id=query.message.message_id,
            reply_markup=inline_main_submit_disable(),
        )

    elif data == SUBSCRIB_DISABLE:
        user_id=update.effective_message.chat_id
        table.setSubscribNotify("false", user_id)
        context.bot.answer_callback_query(callback_query_id=query.id, text="Подписка отменена", show_alert=True)
        context.bot.edit_message_text(
            chat_id=chat_id,
            text=notifyMassage,
            parse_mode=ParseMode.HTML,
            message_id=query.message.message_id,
            reply_markup=inline_main_submit_enable(),
        )
    elif data == BUTTON_INLINE_NOTIFY:
        table.createNotifyTables()
        table.setNotifyUser(chat_id)

        isSubmit = table.getSubmitNotify(chat_id)[0] == "true"
        if isSubmit:
            context.bot.edit_message_text(
                chat_id=chat_id,
                text=notifyMassage,
                parse_mode=ParseMode.HTML,
                message_id=query.message.message_id,
                reply_markup=inline_main_submit_disable()
            )
        else:
            context.bot.edit_message_text(
                chat_id=chat_id,
                text=notifyMassage,
                parse_mode=ParseMode.HTML,
                message_id=query.message.message_id,
                reply_markup=inline_main_submit_enable()
            )

def notify(massage, context: CallbackContext):
    text = massage.replace(notifySecret, '')
    rows = table.getNotifyUsers("true")
    for row in rows:
        context.bot.send_message(
            chat_id = row[0],
            text=text,
            parse_mode=ParseMode.HTML,
        )

def do_start(update: Update, context: CallbackContext):
    text = startMessage
    context.bot.send_message(
        chat_id = update.message.chat_id,
        text='\n'.join(text),
        parse_mode=ParseMode.HTML,
        reply_markup=get_base_inline_keyboard_start(),
    )

def setNewUser(UserId,UserName,KeyUser):
    table.setParticipant(UserId,UserName,"Offline",0,KeyUser)

def updateUser(UserId,UserName,KeyUser):
    table.updateKey(UserId,KeyUser)

def getOnline():
    result = ""
    haveOnline = False
    allData = table.getAllData()
    for x in allData:
        if str(x[3]) == "Online":
            haveOnline = True
            result += "🥷 %s\n🎮 %s сыграно\n🔑 %s\n\n"%(x[2],x[4],x[5])
            # result.append("🤖 %s 🎮 games: %s"%(x[2],x[4]))
    if haveOnline:
        return result
    else:
        return "Нет игроков онлайн"

def getAll(page):
    result = ""
    allData = table.getAllDataViaPage(page)
    size = math.ceil(len(table.getAllData())/15)
    for x in allData:
            result += "🥷 %s\n🔑 %s\n\n"%(x[2],x[5])
            # result.append("🤖 %s 🎮 games: %s"%(x[2],x[4]))
    result += "\nТекущая страница %d из %d"%(page,size)
    return result


def do_echo(update: Update, context: CallbackContext):
    text = update.message.text
    creator = update.message.chat.id

    randomTips = tips

    text_tips = random.choice(randomTips)

    isSubmit = table.getSubmit(creator)[0] == "true"

    if isSubmit:
        table.setSubscrib("false", creator)
        context.bot.send_message(
            chat_id = creator,
            text=moderMassage,
            parse_mode=ParseMode.HTML,
            reply_markup=get_base_inline_keyboard_continue()
        )
        context.bot.send_message(
            chat_id = channel_chat_id,
            text="Сообщение от %s %s (id = %s) \n%s" %(update.message.from_user.first_name, update.message.from_user.last_name, str(update.message.from_user.id), update.message.text),
            parse_mode=ParseMode.HTML
        )
    else:
        resultMassage = list(text.split(" "))

        if resultMassage[0].find(notifySecret) != -1:
            notify(text, context=context)
        else:
            context.bot.send_message(
                chat_id = creator,
                text=text_tips,
                parse_mode=ParseMode.HTML,
                reply_markup=get_base_inline_keyboard_continue()
            )

    if creator == channel_chat_id:
        isAdminMode = True if len(table.isAdminMode()) > 0 else False
        if text == "New" and not isAdminMode:
            context.bot.send_message(
                chat_id = creator,
                text="{\"UserId\":\"_\",\"UserName\":\"_\",\"KeyUser\":\"_\"}",
                parse_mode=ParseMode.HTML
            )
            setNewUser(0000,"UserName","0000")
        elif text == "Cancel":
            table.delRow()
            context.bot.send_message(
                chat_id = creator,
                text="Ввод отменен",
                parse_mode=ParseMode.HTML
            )
        elif text == "AllData":
            try:
                requestParticipants = table.getAllData()
                s = io.StringIO()
                csv.writer(s).writerows(requestParticipants)
                s.seek(0)
                buf = io.BytesIO()
                buf.write(s.getvalue().encode())
                buf.seek(0)
                buf.name = 'report_from_database.csv'
                context.bot.send_document(
                    chat_id=creator,
                    document=buf
                )
            
            except:
                context.bot.send_message(
                    chat_id = creator,
                    text="Error",
                    parse_mode=ParseMode.HTML
                )
        elif text in table.getUserIds():
            table.delUser(text)
            context.bot.send_message(
                chat_id = creator,
                text=u'%s'%(table.getAllData()),
                parse_mode=ParseMode.HTML
            )
        elif isAdminMode and text != "New":
            dataobj = json.loads(text)
            if dataobj["UserId"] in table.getUserIds():
                updateUser(dataobj["UserId"],dataobj["UserName"],dataobj["KeyUser"])
            else:
                setNewUser(dataobj["UserId"],dataobj["UserName"],dataobj["KeyUser"])
            table.delRow()
            context.bot.send_message(
                chat_id = creator,
                text=table.getUser(dataobj["UserId"]),
                parse_mode=ParseMode.HTML
            )

def main():
    print ("Starting bot...")

    req = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
    )
    bot = Bot(
        token="",
        request=req,
    )
    updater = Updater(
        bot=bot,
        use_context=True,
    )

    # Проверить что бот корректно подключился к Telegram API
    print ("---------------------------")

    # Навесить обработчики команд
    start_handler = CommandHandler("start", do_start)
    message_handler = MessageHandler(Filters.text, do_echo)
    buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler)

    updater.dispatcher.add_handler(start_handler)
    updater.dispatcher.add_handler(message_handler)
    updater.dispatcher.add_handler(buttons_handler)

    # Начать бесконечную обработку входящих сообщений
    updater.start_polling()
    updater.idle()

    print ("Finished work...")

if __name__ == '__main__':
    main()
