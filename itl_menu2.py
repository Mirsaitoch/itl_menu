import telebot
from telebot import types
from datetime import datetime, date, time
import requests
import random
import sqlite3
con = sqlite3.connect('menu.db', check_same_thread=False)
api_link = "http://192.168.43.250:8000/api/getMenu"
cur = con.cursor()
bot = telebot.TeleBot(token="1155683546:AAGP_jrQKn0RGr3MKeiW5B1pvOZYAWTHork")
day_ = ""
ch = 0
tf = 1
meal_time = ""
chetnoct_week = 0
monday = types.KeyboardButton('Понедельник')
tuesday = types.KeyboardButton('Вторник')
wednesday = types.KeyboardButton('Среда')
thursday = types.KeyboardButton('Четверг')
friday = types.KeyboardButton('Пятница')
saturday = types.KeyboardButton('Суббота')
sunday = types.KeyboardButton('Воскресенье')
breakfast = types.KeyboardButton('Завтрак 🍚')
second_breakfast = types.KeyboardButton('Второй завтрак 🥐')
lunch = types.KeyboardButton('Обед 🍝')
snack = types.KeyboardButton('Полдник 🍪')
dinner = types.KeyboardButton('Ужин 🍲')
back1 = types.KeyboardButton("Назад 🔙")
days_of_week = types.ReplyKeyboardMarkup()
meal = types.ReplyKeyboardMarkup()
days_of_week.row(monday, tuesday, wednesday)
days_of_week.row(thursday, friday, saturday)
days_of_week.row(sunday)
meal.row(breakfast, second_breakfast, lunch)
meal.row(snack, dinner, back1)
hide = types.ReplyKeyboardRemove()


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привет! Нажми на день недели, чтобы посмотреть меню", reply_markup=days_of_week)
    bot.register_next_step_handler(message, day)


def day(message):
    global day_, ch, chetnoct_week, t_f
    id_day = int(date.today().isoweekday())
    if id_day == 1 and ch == 0:
        ch = 1
        chetnoct_week += 1
    if id_day != 1:
        ch = 0
    if chetnoct_week % 2 != 0:
        t_f = 1
    if chetnoct_week % 2 == 0:
        t_f = 1
    if message.text == 'Понедельник':
        day_ = "Monday"
    if message.text == 'Вторник':
        day_ = "Tuesday"
    if message.text == 'Среда':
        day_ = "Wednesday"
    if message.text == 'Четверг':
        day_ = "Thursday"
    if message.text == 'Пятница':
        day_ = "Friday"
    if message.text == 'Суббота':
        day_ = "Saturday"
    if message.text == 'Воскресенье':
        day_ = "Sunday"
    bot.send_message(message.chat.id, "Какой прием пищи Вас интересует?", reply_markup=meal)
    bot.register_next_step_handler(message, food)


def food(message):
    global day_, t_f, meal_time
    if message.text == 'Завтрак 🍚':
        meal_time = "1"
        send(message)
    if message.text == 'Второй завтрак 🥐':
        meal_time = "2"
        send(message)
    if message.text == 'Обед 🍝':
        meal_time = "3"
        send(message)
    if message.text == 'Полдник 🍪':
        meal_time = "4"
        send(message)
    if message.text == 'Ужин 🍲':
        meal_time = "5"
        send(message)
    if message.text == "Назад 🔙":
        bot.send_message(message.chat.id, "Выберите день недели", reply_markup=days_of_week)
        bot.register_next_step_handler(message, day)


def send(message):
    global day_, t_f, meal_time
    resp = requests.post(api_link, data={
        'day_name': day_,
        'menu_id': t_f,
        'meal_type': meal_time
    })
    resp = resp.json()
    result = resp["meals"]
    fr = (result.split(","))
    text = ""
    for i in fr:
        text += ("✅" + i + "\n")
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, food)


bot.polling(none_stop=True)