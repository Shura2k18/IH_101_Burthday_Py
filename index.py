from webserver import keep_alive
from text import members
import asyncio
import moment
import pymongo
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InputFile
import random
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

db_client = pymongo.MongoClient(os.getenv('MONGO_URL'))
current_db = db_client['myFirstDatabase']
collection = current_db['chats1']

chats = []
for coll in collection.find():
    chats.append(coll)

async def remind(chatId, name, month, day):
    year = moment.utcnow().timezone("Europe/Kiev").year
    time = moment.utcnow().timezone("Europe/Kiev").date
    timed = moment.date(year, month, day, 12, 8).locale("Europe/Kiev").timezone("Europe/Kiev")
    if timed < time:
        year += 1
        endTime = timed.clone().add(years=1)
    else:
        endTime = moment.date(year, month, day, 12, 8).locale("Europe/Kiev").timezone("Europe/Kiev")
    while True:
        now = moment.utcnow().timezone("Europe/Kiev").date
        if now >= endTime:
            num = random.randint(0,4)
            # Send reminder message
            if month == 3 and day == 16:
                image = InputFile('img/newyear.jpg')
                await bot.send_photo(chatId, image, "\u2764\ufe0f \u2764\ufe0f \u2764\ufe0f \nЛюбі друзі, у цей чудовий день хотілось би привітати вас всіх з Новий роком та побажати щастя, здоров'я, успіхів у житті й мирного неба над головою\U0001F1FA\U0001F1E6))) \nЗі святом!!!!!!!\U0001f389 \U0001f389 \U0001f389")
            elif month == 1 and day == 1:
                image = InputFile('img/march.jpg')
                await bot.send_photo(chatId, image, "\u2764\ufe0f \u2764\ufe0f \u2764\ufe0f \nЛюбі дівчата, вітаю зі святом жіночої краси і чарівності, весняного натхнення і світлої радості! У день 8 березня від щирого серця бажаю постійного відчуття щастя, щоденної радості в душі, чарівних почуттів любові і ніжності, хорошого настрою і впевненості в собі!))) \nЗі святом!!!!!!!\U0001f337 \U0001f337 \U0001f337")
            else:
                image = InputFile('img/'+ str(num) +'.jpg')
                await bot.send_photo(chatId, image, "\u2764\ufe0f \u2764\ufe0f \u2764\ufe0f \nЛюбі друзі, у цей чудовий день хотілось би привітати, " + name + " з днем народження та побажати щастя, здоров'я, успіхів у житті й мирного неба над головою\U0001F1FA\U0001F1E6))) \nЗі святом!!!!!!!\U0001f389 \U0001f389 \U0001f389")
            # Add a new reminder for the next cycle
            endTime = endTime.clone().add(years=1)
            year += 1
        await asyncio.sleep(60) # Wait for 60 seconds before checking again


API_TOKEN = os.getenv('API_TOKEN')

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)




@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    first_name = str(message.from_user['first_name'])
    last_name = " " + str(message.from_user['last_name']) if message.from_user['last_name'] != None else ""
    username = " " + str(message.from_user['username']) if message.from_user['username'] != None else ""
    name1 = first_name + last_name + username
    name2 = first_name + last_name
    title = message.chat.title if message.chat.title else name1 + ' chat'

    isAvailable = any( chat['chatId'] == round(message.chat.id) for chat in chats )
    if not isAvailable:
        await message.answer('Дякую, що запустили бота)')
        for member in members:
            asyncio.create_task(remind(round(message.chat.id), member['name'], member['month'], member['day']))
        await bot.send_message(624965724, 'Fuck: ID: ' + str(round(message.chat.id)) + ', Who activeted: ' + name1 + ', Title: ' + title)
        data = {'chatId': round(message.chat.id), 'username': name1, 'title': title}
        chats.append(data)
        collection.insert_one(data)
    else:
        await message.answer(name2 + ', чого тобі треба')
        await bot.send_message(624965724, 'Hui ' + str(round(message.chat.id)) + ' ' + name1 + ' ' + title)

@dp.message_handler(commands=['startGroup'])
async def start_group(message: types.Message):
    isAvailable = any( chat['chatId'] == round(message.chat.id) for chat in chats )
    if not isAvailable:
        await message.answer('Ви запустили бота для групи')
        for member in members:
            asyncio.create_task(remind(-1001544778674, member['name'], member['month'], member['day']))
        await bot.send_message(624965724, 'Fuck: ID: ' + str(round(message.chat.id)) + ', Who activeted: ' + "It's me" + ', Title: ' + 'Our group')
        data = {'chatId': -1001544778674, 'username': "It's me", 'title': 'Our group'}
        chats.append(data)
        collection.insert_one(data)
    else:
        await message.answer('Вже запущений')

@dp.message_handler(commands=['getChats'])
async def get_chats(message: types.Message):
    if chats:
        for chat in chats:
            await message.answer('ID: ' + str(round(chat['chatId'])) + ', Who activeted: ' + chat['username'] + ', Title: ' + chat['title'])
    else:
        await message.answer('Чатів не знайдено(')

@dp.message_handler(commands=['say'])
async def say(message: types.Message):
    first_name = str(message.from_user['first_name'])
    last_name = " " + str(message.from_user['last_name']) if message.from_user['last_name'] != None else ""
    username = " @" + str(message.from_user['username']) if message.from_user['username'] != None else ""
    name = first_name + last_name + username
    args = message.text.split()
    args.pop(0)
    arg = ''
    for a in args:
        arg = arg + a + " "
    await bot.send_message(624965724, name + " " + str(round(message.chat.id)) + " СКАЗАВ: " + arg)

@dp.message_handler(commands=['send'])
async def send(message: types.Message):
    args = message.text.split()
    args.pop(0)
    to = args[0]
    args.pop(0)
    arg = ''
    for a in args:
        arg = arg + a + " "
    await bot.send_message(to, arg)


async def on_startup(dp):
    for chat in chats:
        for member in members:
            asyncio.create_task(remind(round(chat['chatId']), member['name'], member['month'], member['day']))

keep_alive()

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)