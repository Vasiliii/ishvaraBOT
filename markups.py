from aiogram import types
import config

btnBOT = types.InlineKeyboardButton("Мой дом", url= config.bot_URL)
btnCh_URL = types.InlineKeyboardButton("Инвестиции без границ", url= config.chanel_URL)
chanelMenu = types.InlineKeyboardMarkup(row_width=1)
botMenu = types.InlineKeyboardMarkup(row_width=1)
botMenu.insert(btnBOT)
chanelMenu.insert(btnCh_URL)