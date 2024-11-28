from path import hreport_key
from telebot.async_telebot import AsyncTeleBot
import asyncio
bot =  AsyncTeleBot(hreport_key)
from google_task import res
import pandas as pd
import os
from flask import Flask
from telebot import types


app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from Render!"



@bot.message_handler(commands=['start'])
async def send_welcom(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Xodimlar", callback_data='xodim'), row_width=1)
    markup.add(types.InlineKeyboardButton("Xizmat xati", callback_data='xat'), row_width=1)
    markup.add(types.InlineKeyboardButton("Buyruqlar", callback_data='buyruq'), row_width=1)
    text = "Hush kelibsiz! Ishni boshlash uchun quyidagilardan biri tanlang"
    await bot.send_message(message.chat.id, text, reply_markup=markup)



@bot.callback_query_handler(func=lambda xat: xat.data == 'xat')
async def get_xatlar(xat):
     await bot.send_message(xat.message.chat.id, "siz xizmatni kiriting... oxirgi 5 ta xarfni")


@bot.message_handler(content_types=['text'])
async def xat_message_handler(message):
    result = res[res['nomer'].str.len()>7]    
    
    text = result.loc[result['nomer'].str.endswith(message.text)]
    text = text[['nomer', 'Status','Natijasi']]
    text = text.reset_index(drop=True)
    text.index.rename('№', inplace=True)
    #result = res['nomer']
    await bot.reply_to(message, f"Sizning xizmat xatingiz: {text}")   


@bot.callback_query_handler(func=lambda call: call.data == 'xodim' )
async def callback(call):
    await bot.answer_callback_query(call.id, text="Thanks for clicked")

    xodimlar = ['Qodirov', "Nurmatov", 'Toshmatov', 'Madaminov', 'Abdusalomov','Mamarasulov']
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(xodimlar[0], callback_data="Qodirov A"))
    markup.add(types.InlineKeyboardButton(xodimlar[1], callback_data="Nurmatov E"))
    markup.add(types.InlineKeyboardButton(xodimlar[2], callback_data="Toshmatov F"))
    markup.add(types.InlineKeyboardButton(xodimlar[3], callback_data="Madaminov I"))
    markup.add(types.InlineKeyboardButton(xodimlar[4], callback_data="Abdusalomov J"))
    markup.add(types.InlineKeyboardButton(xodimlar[5], callback_data="Mamarasulov Sh"))
   
    await bot.send_message(call.message.chat.id, "xodimni tanlang",reply_markup=markup)
    #await bot.register_inline_handler(call, get_tasks)
    #get_tasks(call.message)



@bot.callback_query_handler(func= lambda call: True)
async def handle_callback_quer(call):
    xodimlar = res['javobgar'].values.tolist()
    xodimlar = list(set(xodimlar))
    xodim = call.data

    if xodim in xodimlar:    
            text = res.loc[res['javobgar'].str.contains(xodim)]
            text = text[['nomer', 'Status']]
            text = text.reset_index(drop=True)
            text.index.rename('№', inplace=True)
        
    #if call.data == 'Nurmatov E':
            await bot.send_message(call.message.chat.id, text=text)
    else:
       
       await bot.send_message(call.message.chat.id, "Bunday xodim bizda ishlamaydi.")

# Render tomonidan berilgan portni olish
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

asyncio.run(bot.polling())

