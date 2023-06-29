from  aiogram import Bot, Dispatcher, executor, types 
import config
import markups as nav

bot = Bot(config.Token)
dp = Dispatcher(bot)

def checkSubChanel(chat_member):
    return chat_member['status'] != "left"
    
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Hello!")
    
@dp.message_handler(commands=['test'], commands_prefix = '!')
async def test(message: types.Message):
    await message.reply(message.from_user.id)

    
@dp.message_handler(content_types=['text'])
async def textFilter(message: types.Message):
    if checkSubChanel(await bot.get_chat_member(chat_id=config.chanel_id, user_id=message.from_user.id)):
        lower_message = message.text.lower()
        for spam in config.spam:
                if spam in lower_message.lower():
                    await message.forward(config.delGroup_id)
                    await message.delete()
                    break
        for keyword in config.estate:
                if keyword in lower_message.lower():
                    await message.answer(f'{message.from_user.first_name}Вы можете разместить объявление по недвижимости только через публикацию объявления в нашем боте "МойДом"',reply_markup=nav.botMenu)
                    await message.delete() 
                    break
        for bad_word in config.swears:
            if bad_word in lower_message:
                await message.answer("Запрещено сквернословить вы заглушены на 6 часов")
                await message.delete()
                break
    else:
        await message.forward(config.delGroup_id)
        await message.answer(f"{message.from_user.first_name}, для того, что бы опубликовать объявление в группе Вам необходимо подписаться на наш канал 👇️",reply_markup=nav.chanelMenu)
        await message.delete()
        
@dp.message_handler(content_types=['photo'])
async def photoFilter(message: types.Message):
    if checkSubChanel(await bot.get_chat_member(chat_id=config.chanel_id, user_id=message.from_user.id)):
        lower_message = message.text.lower()
        for spam in config.spam:
                if spam in lower_message.lower():
                    await message.forward(config.delGroup_id)
                    await message.delete()
                    break
        for keyword in config.estate:
                if keyword in lower_message.lower():
                    await message.answer(f'{message.from_user.first_name}Вы можете разместить объявление по недвижимости только через публикацию объявления в нашем боте "МойДом"',reply_markup=nav.botMenu)
                    await message.delete() 
                    break
        for bad_word in config.swears:
            if bad_word in lower_message:
                await message.answer("Запрещено сквернословить вы заглушены на 6 часов")
                await message.delete()
                break
    else:
        await message.forward(config.delGroup_id)
        await message.answer(f"{message.from_user.first_name}, для того, что бы опубликовать объявление в группе Вам необходимо подписаться на наш канал 👇️",reply_markup=nav.chanelMenu)
        await message.delete()
        


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)