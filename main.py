from  aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ChatType
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import filters
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
import config
import markups as nav
from db import DataBase

bot = Bot(config.Token)
dp = Dispatcher(bot, storage=MemoryStorage())
db = DataBase('dataBase.db')
scheduler = AsyncIOScheduler(timezone = 'Europe/Moscow')

class UserReg(StatesGroup):
    login = State()
    pasword = State()
    checkLog = State()
    checkPass = State()
    add_advertisement = State()

def checkSubChanel(chat_member):
    return chat_member['status'] != "left"

def checkAdmin(user_id):
    check = str(user_id)
    for id in config.admin_id:
        if id in check:
            return True
        else: 
            return False

async def delete(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
        
async def answerTxt(message: types.Message, state = FSMContext):
    if message.chat.type == ChatType.SUPERGROUP:
        if not db.check_warning(message.from_user.id):
            if not db.nights():  
                if not db.mute(message.from_user.id):
                    if checkSubChanel(await bot.get_chat_member(chat_id=config.chanel_id, user_id=message.from_user.id)) and filters.AdminFilter():
                        lower_message = message.text.lower()
                        for spam in config.spam:
                            if spam in lower_message.lower():
                                    if not db.check_warning(message.from_user.id):
                                        db.warning(message.from_user.id)
                                        await message.forward(config.delGroup_id)
                                        message1 = await message.answer("Рекламные объявления являются платной опцией, обратитесь к администратору @Nikita_Kononenko")
                                        scheduler.add_job(delete, trigger='date', run_date = datetime.now() + timedelta(seconds=180), kwargs={'message': message1})
                                        await message.delete()
                                        break
                                    else:
                                        await message.bot.ban_chat_member(message.chat.id, message.from_user.id)
                                        await message.delete()
                        for keyword in config.estate:
                            if keyword in lower_message.lower() and checkAdmin(message.from_user.id) != True:
                                    message2 = await message.answer(f'{message.from_user.first_name}, Вы можете разместить объявление по недвижимости только через публикацию объявления в нашем боте "МойДом"',reply_markup=nav.botMenu)
                                    scheduler.add_job(delete, trigger='date', run_date = datetime.now() + timedelta(seconds=180), kwargs={'message': message2})
                                    await message.delete() 
                                    break
                        for bad_word in config.swears:
                            if bad_word in lower_message:
                                message3 = await message.answer("Нецензурные выражения в нашем чате запрещены вы заглушены на 6 часов")
                                scheduler.add_job(delete, trigger='date', run_date = datetime.now() + timedelta(seconds=180), kwargs={'message': message3})
                                db.add_mute(message.from_user.id,6)
                                await message.delete()
                                break
                    
                    elif message.from_user.id != config.bot_ignore_message and checkAdmin(message.from_user.id) != True:
                        db.warning(message.from_user.id)
                        await message.forward(config.delGroup_id)
                        message4 = await message.answer(f"{message.from_user.first_name}, для того, что бы опубликовать объявление в группе Вам необходимо подписаться на наш канал 👇️",reply_markup=nav.chanelMenu)
                        scheduler.add_job(delete, trigger='date', run_date = datetime.now() + timedelta(seconds=180), kwargs={'message': message4})
                        await message.delete()
                else:
                    await message.forward(config.delGroup_id)
                    await message.delete()
                    
            else:
                db.warning(message.from_user.id)
                message5 = await message.answer("Нельзя писать ночью")
                scheduler.add_job(delete, trigger='date', run_date = datetime.now() + timedelta(seconds=180), kwargs={'message': message5})
                await message.delete()     
        else:
            await message.bot.ban_chat_member(message.chat.id, message.from_user.id)
            await message.delete()
            
    elif message.chat.type == ChatType.PRIVATE:
        text = message.text
        if text.lower() == 'зарегистрироваться':
            if not db.user_exists(message.from_user.id):
                db.add_user(message.from_user.id, message.from_user.full_name)
                await message.answer("Придумайте логин:")
                await UserReg.login.set()
        elif text.lower() == 'войти':
            if not db.user_exists(message.from_user.id):
                await message.answer("Введите ваш логин:")
                await UserReg.checkLog.set()
            else:
                await bot.send_message(message.chat.id,"Вы успешно вошли", reply_markup=nav.userMenu)       
        else:
            await message.answer("Войдете или зарегистрируйтесь", reply_markup= nav.privateMenu)

async def answerPhoto(message: types.Message, state = FSMContext):
    if message.chat.type == ChatType.SUPERGROUP:
        if not db.check_warning(message.from_user.id):
            if not db.nights():  
                if not db.mute(message.from_user.id):
                    if checkSubChanel(await bot.get_chat_member(chat_id=config.chanel_id, user_id=message.from_user.id)) and message.from_user.id != config.bot_ignore_message:
                        lower_message = message.caption
                        lower_message.lower()
                        for spam in config.spam:
                            if spam in lower_message.lower():
                                    if not db.check_warning(message.from_user.id):
                                        db.warning(message.from_user.id)
                                        await message.forward(config.delGroup_id)
                                        message1= await message.answer("Рекламные объявления являются платной опцией, обратитесь к администратору @Nikita_Kononenko")
                                        scheduler.add_job(delete, trigger='date', run_date = datetime.now() + timedelta(seconds=180), kwargs={'message': message1})
                                        await message.delete()
                                        break
                                    else:
                                        await message.bot.ban_chat_member(message.chat.id, message.from_user.id)
                                        await message.delete()
                        for keyword in config.estate:
                            if keyword in lower_message.lower() and checkAdmin(message.from_user.id) != True:
                                    message2 = await message.answer(f'{message.from_user.first_name}, Вы можете разместить объявление по недвижимости только через публикацию объявления в нашем боте "МойДом"',reply_markup=nav.botMenu)
                                    scheduler.add_job(delete, trigger='date', run_date = datetime.now() + timedelta(seconds=180), kwargs={'message': message2})
                                    await message.delete() 
                                    break
                        for bad_word in config.swears:
                            if bad_word in lower_message:
                                message3 = await message.answer("Нецензурные выражения в нашем чате запрещены вы заглушены на 6 часов")
                                scheduler.add_job(delete, trigger='date', run_date = datetime.now() + timedelta(seconds=180), kwargs={'message': message3})
                                db.add_mute(message.from_user.id,6)
                                await message.delete()
                                break
                    
                    elif message.from_user.id != config.bot_ignore_message and checkAdmin(message.from_user.id) != True:
                        db.warning(message.from_user.id)
                        await message.forward(config.delGroup_id)
                        message4 = await message.answer(f"{message.from_user.first_name}, для того, что бы опубликовать объявление в группе Вам необходимо подписаться на наш канал 👇️",reply_markup=nav.chanelMenu)
                        scheduler.add_job(delete, trigger='date', run_date = datetime.now() + timedelta(seconds=180), kwargs={'message': message4})
                        await message.delete()
                else:
                    await message.forward(config.delGroup_id)
                    await message.delete()
                    
            else:
                db.warning(message.from_user.id)
                message5 = await message.answer("Нельзя писать ночью")
                scheduler.add_job(delete, trigger='date', run_date = datetime.now() + timedelta(seconds=180),  kwargs={'message': message5})
                await message.delete()     
        else:
            await message.bot.ban_chat_member(message.chat.id, message.from_user.id)
            await message.delete()
            
    elif message.chat.type == ChatType.PRIVATE:
        text = message.caption
        if text.lower() == 'зарегистрироваться':
            if not db.user_exists(message.from_user.id):
                db.add_user(message.from_user.id, message.from_user.full_name)
                await message.answer("Придумайте логин:")
                await UserReg.login.set()
        elif text.lower() == 'войти':
            if not db.user_exists(message.from_user.id):
                await message.answer("Введите ваш логин:")
                await UserReg.checkLog.set()
        else:
            await message.answer("Войдете или зарегистрируйтесь", reply_markup= nav.privateMenu)

async def nightsMode():
    db.add_nights(9)
    await bot.send_message(config.group_id,"Отправка сообщений ограничена с 22:00 до 7:00")
    print("Функция ночного режима включилась")

scheduler.add_job(nightsMode, trigger='cron', hour = 22 , minute = 00, start_date = datetime.now())

@dp.callback_query_handler()
async def change_login(callback: types.CallbackQuery):
    if callback.data == 'change_log':
        await UserReg.login.set()
        await bot.send_message(callback.from_user.id, "Придумайте новый логин")
    elif callback.data == 'add_advertisement':
        #await UserReg.add_advertisement.set()
        await callback.message.edit_text("Выберете группы в которых хотите оппубликовать ваше сообщение", reply_markup=nav.marAdd_groups)
     
    
@dp.message_handler(state=UserReg.add_advertisement)
async def advertisement(message: types.Message, state = FSMContext):
    await state.finish()
    await message.forward(config.group_id[0])

@dp.message_handler(state=UserReg.login)
async def add_login(message: types.Message, state = FSMContext):
    login = message.text
    user_id = message.from_user.id
    if not db.check_log(login):
        await state.finish()
        db.add_log(user_id, login)
        await message.answer("Придуймайте пароль:")
        await UserReg.pasword.set()
    else: 
        await message.answer("Такой логин уже есть попробуйте другой")
        await UserReg.login.set()
        
@dp.message_handler(state=UserReg.pasword)
async def add_pass(message: types.Message, state = FSMContext):
    password = message.text
    user_id = message.from_user.id
    await state.finish()
    db.add_pass(user_id, password)
    await message.answer("Вы успешно зарегистрировались", reply_markup= nav.userMenu)

@dp.message_handler(state=UserReg.checkLog)
async def check_log(message: types.Message, state = FSMContext):
    login = message.text
    if db.check_log(login):
        await state.finish()
        await message.answer("Введите пароль:")
        await UserReg.checkPass.set()
    else:
        await message.answer("Мы не нашли учётную запись с таким логином\nПопробуйте снова ввести логин")
        await UserReg.checkLog.set()

@dp.message_handler(state=UserReg.checkPass)
async def check_Pass(message: types.Message, state = FSMContext):
    login = message.text
    if db.check_pass( login):
        await state.finish()
        await message.answer("Вы успешно вошли", reply_markup= nav.userMenu)
    else:
        await message.answer("Пароль не подходит\nПопробуйте снова ввести пароль")
        await UserReg.checkPass.set()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == ChatType.PRIVATE:
        await message.answer("Hello!", reply_markup = nav.privateMenu)
    
@dp.message_handler(commands=['test'], commands_prefix = '!')
async def test(message: types.Message):
    await message.reply(message.from_user.id)
    
@dp.message_handler(commands=['mute'], commands_prefix = '!')
async def mute(message : types.Message):
    if checkAdmin(message.from_user.id):
        if not message.reply_to_message:
            await message.reply("Команда должна быть ответом на сообщение")
            return
        mute_hours = message.text[6:]
        if str(mute_hours) == '':
            await message.answer("Вы забыли указать время заглушения!")
            await message.delete()
        else:
            db.add_mute(message.reply_to_message.from_user.id, int(mute_hours))
            await message.bot.delete_message(message.chat.id, message.message_id) 
            await message.bot.delete_message(message.chat.id, message.reply_to_message.message_id)
            await message.answer(f"{message.from_user.full_name} были заглушены на {mute_hours} часов")
    else: 
        await message.answer("Только админы могут использовать команды")
        await message.delete()
        
@dp.message_handler(commands=['unmute'], commands_prefix = '!')
async def unmute(message : types.Message):
    if checkAdmin(message.from_user.id):
        people_name = message.text[8:]
        if not people_name:
            await message.reply("Команда должна содержать полное  имя пользователя")
            return
        db.unmute(people_name)
        await message.answer(f"Пользователь {people_name} снова может писать")
    else: 
        await message.answer("Только админы могут использовать команды")
        await message.delete()

@dp.message_handler(commands=['ban'], commands_prefix = '!')
async def ban(message: types.Message):
    if checkAdmin(message.from_user.id):
        if not message.reply_to_message:
            await message.reply("Команда должна быть ответом на сообщение")
            return
        else:
            await message.bot.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)
    else: 
        await message.answer("Только админы могут использовать команды")
        await message.delete()

@dp.message_handler(commands=['swear'], commands_prefix = '!')#add to swear dict
async def swear(message: types.Message):
    if checkAdmin(message.from_user.id):
        new_swear = message.text[7:]
        config.swears.append(new_swear)
        await message.delete()
    else: 
        await message.answer("Только админы могут использовать команды")
        await message.delete()

@dp.message_handler(commands=['estate'], commands_prefix = '!')#add to estates dict
async def estate(message: types.Message):
    if checkAdmin(message.from_user.id):
        new_estate = message.text[8:]
        config.estate.append(new_estate)
        await message.delete()
    else: 
        await message.answer("Только админы могут использовать команды")
        await message.delete()

@dp.message_handler(commands=['spam'], commands_prefix = '!')#add to spam dict
async def spam(message: types.Message):
    if checkAdmin(message.from_user.id):
        new_spam = message.text[5:]
        config.spam.append(new_spam)
        await message.delete()
    else: 
        await message.answer("Только админы могут использовать команды")
        await message.delete()
    
@dp.message_handler(content_types=['text'])
async def textFilter(message: types.Message, state = FSMContext):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id, message.from_user.full_name)
        await answerTxt(message)
    else:
        await answerTxt(message)
                        
@dp.message_handler(content_types=['photo'])
async def photoFilter(message: types.Message, state = FSMContext):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id, message.from_user.full_name)   
        await answerPhoto(message)
    else: 
        await answerPhoto(message)

scheduler.start()           
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)