from aiogram import types
import config

#inline button
add_advertisement = types.InlineKeyboardButton("Добавить объявление", callback_data = 'add_advertisement')
change_login = types.InlineKeyboardButton(" Изменить логин и пароль", callback_data= 'change_log')
userMenu = types.InlineKeyboardMarkup(row_width=2)
userMenu.add(add_advertisement, change_login)

btnAdd_Groups0 = types.InlineKeyboardButton("Тест группа1", callback_data= 'testGroup1')
btnAdd_Groups1 = types.InlineKeyboardButton("Тест группа2", callback_data= 'testGroup2')
btnAdd_Groups2 = types.InlineKeyboardButton("Тест группа3", callback_data= 'testGroup3')
btnAdd_Groups3 = types.InlineKeyboardButton("Тест группа4", callback_data= 'testGroup4')
btnAdd_Groups4 = types.InlineKeyboardButton("Тест группа5", callback_data= 'testGroup5')

marAdd_groups = types.InlineKeyboardMarkup(row_width=1)
marAdd_groups.add(btnAdd_Groups0,btnAdd_Groups1,btnAdd_Groups2,btnAdd_Groups3,btnAdd_Groups4)

btnBOT = types.InlineKeyboardButton("Мой дом", url= config.bot_URL)
btnCh_URL = types.InlineKeyboardButton("Инвестиции без границ", url= config.chanel_URL)
chanelMenu = types.InlineKeyboardMarkup(row_width=1)
botMenu = types.InlineKeyboardMarkup(row_width=1)
botMenu.insert(btnBOT)
chanelMenu.insert(btnCh_URL)

#reply button
auth = types.KeyboardButton("Войти")
reg = types.KeyboardButton("Зарегистрироваться")
privateMenu = types.ReplyKeyboardMarkup(resize_keyboard= True ,row_width = 2)
privateMenu.add(reg, auth)