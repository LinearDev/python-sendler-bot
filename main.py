import logging

import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

logging.basicConfig(level=logging.INFO)

from db import Database

#5529982744:AAF5FUgJE05d9DN6CdtvZPRpV5yPD4wAM-U 5196084873:AAFC9TjmqO-dr5mVLTFoun6h5do9W-amPss
bot = Bot(token="5196084873:AAFC9TjmqO-dr5mVLTFoun6h5do9W-amPss")
storage=MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database('database.db')

class Form(StatesGroup):
    text=State()
    but_state=State()
    but_text=State()
    but_link=State()
    send_without_but=State()

inline_kb = InlineKeyboardMarkup(row_width=1)
inline_hello_btn = InlineKeyboardButton(text='ССЫЛКА', url="https://t.me/+T91wk9C0v_A3OTIy")
inline_kb.add(inline_hello_btn)

#send a start message
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == "private":
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
        await bot.send_photo(message.from_user.id, photo=open('hello_img.jpg', 'rb'))
        
        await bot.send_message(
            message.from_user.id,
            "***В ОЧЕРЕДНОЙ РАЗ РЕКОМЕНДУЮ КАНАЛ МОЕГО ЗНАКОМОГО, ВИДЕЛ ЕГО ВЫИГРЫШИ ЛИЧНО😉***\n\nЗнаю, что каждый из Вас интересуется ставками и каждому интересен постоянный заработок на них! Сейчас советую Вам действительно профессионала своего дела,[ дядя Дима долгое время занимается аналитикой и ](https://t.me/+T91wk9C0v_A3OTIy) зарабатывает только на беттинге! Честно ведёт канал уже два года, показывает каждый матч на который ставит и зарабатывает, ниже его открытая статистика 👇🏻\n\n✅ КФ 7.10 ( +46.000₽ прибыли)\n✅ КФ 6.50  ( +25.230₽ прибыли)\n🚫 КФ 5.29 ( -5.000₽)\n✅ КФ 5.46 ( + 21.330₽ прибыли)\n\nКАНАЛ ЗАКРЫТЫЙ, НАЙТИ ПОТОМ В ПОИСКЕ ВОЗМОЖНОСТИ НЕ БУДЕТ, ПОЭТОМУ ОБЯЗАТЕЛЬНО ЗАЙДИ, ПОДПИШИСЬ И ИЗУЧИ!🧠👇🏻",
            parse_mode='Markdown',
            reply_markup=inline_kb
        )

#start of filling form for message
@dp.message_handler(commands=['message'])
async def start(message: types.Message):
    if message.chat.type == "private":
        if db.get_admins(message.from_user.id):
            await bot.send_message(message.from_user.id, "Введи текст для сообщения")
            await Form.text.set()
        else:
            pass

#case if user dont want send message
@dp.message_handler(state='*', commands=['cancel'])
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    
    await state.finish()
    await bot.send_message(message.from_user.id, 'Заполнение формы остановлено')

#reply for message text
@dp.message_handler(state=Form.text)
async def message_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text

    await Form.next()
    await bot.send_message(message.from_user.id, 'Будет ли кнопка-ссылка? (yes, no)')

#reply for message question for message button
@dp.message_handler(state=Form.but_state)
async def message_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['but_state'] = message.text

        if message.text == 'yes':
            await Form.next()
            await bot.send_message(message.from_user.id, 'Текст кнопки')
        else:
            users = db.get_users()
            for row in users:
                try:
                    if int(row[1]) != 1:
                        db.set_active(row[0], 1)
                    await bot.send_message(row[0], data['text'], parse_mode='Markdown')
                except:
                    db.set_active(row[0], 0)
            await bot.send_message(message.from_user.id, 'Send Success!')
            await state.finish()

#fill a button cover text
@dp.message_handler(state=Form.but_text)
async def btn_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['but_text'] = message.text
    
    await Form.next()
    await bot.send_message(message.from_user.id, 'Введите ссылку для кнопки')

#add link for button
@dp.message_handler(state=Form.but_link)
async def btn_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['but_link'] = message.text

        spamm_link = InlineKeyboardMarkup(row_width=1)
        spamm_link_btn = InlineKeyboardButton(text=data['but_text'], url=data['but_link'])
        spamm_link.add(spamm_link_btn)

        users = db.get_users()
        for row in users:
            try:
                if int(row[1]) != 1:
                    db.set_active(row[0], 1)
                await bot.send_message(row[0], data['text'], reply_markup=spamm_link, parse_mode='Markdown')
            except:
                db.set_active(row[0], 0)
        await bot.send_message(message.from_user.id, 'Send Success!')
        await state.finish()

#command for adding admins
@dp.message_handler(commands=['add_admin'])
async def add_admin(message: types.Message):
    if db.get_admins(message.from_user.id):
        db.add_admin(message.text[11:])
        await bot.send_message(message.from_user.id, "Admin by ID: "+message.text[11:]+" add to database")
    else:
        pass

#get users
@dp.message_handler(commands=['users'])
async def get_count(message: types.Message):
    if db.get_admins(message.from_user.id):
        user_count = str(db.get_user_count()).replace("(", '').replace(")", '').replace("[", '').replace("]", '').replace(",", '')
        active_users = str(db.get_user_count()).replace("(", '').replace(")", '').replace("[", '').replace("]", '').replace(",", '')
        await bot.send_message(message.from_user.id, "Users in bot: "+user_count+"\nActive users: "+active_users)

#send data base file
@dp.message_handler(commands=['get_database'])
async def get_database(message: types.Message):
    if db.get_admins(message.from_user.id):
        await bot.send_document(message.from_user.id, open('database.db', 'rb'))

#main entry point
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = True)