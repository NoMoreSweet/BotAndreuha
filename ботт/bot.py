import os
import math
import telebot
from telebot import types
import config
import requests, json

bot = telebot.TeleBot(config.TELEGRAM_API_KEY)
# прописать в терманале: pip install telebot
def weather(city, API_KEY):
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    URL = BASE_URL + "q=" + city + "&appid=" + API_KEY
    response = requests.get(URL,
                            params={'units': 'metric', 'lang': 'ru'})
    if response.status_code == 200:
        data = response.json()
        weather_description = data["weather"][0]["main"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        return temperature, humidity, pressure, wind
    else:
        print()

@bot.message_handler(commands=['start'])
def start_message(message):
    msg = bot.reply_to(message, f"Здравствуйте, <b><u>{message.from_user.username}</u></b>! Я - бот показывающий текущую погоду \U0001F31E по городу.", parse_mode='html')
    bot.send_message(message.chat.id, "Введите название города, чтобы продолжить")
    bot.register_next_step_handler(msg, print_weather)
def print_weather(message):
    city = message.text
    temperature = weather(city, config.WEATHER_API_KEY)
    humidity = weather(city, config.WEATHER_API_KEY)
    pressure = weather(city, config.WEATHER_API_KEY)
    wind = weather(city, config.WEATHER_API_KEY)
    msg = bot.reply_to(message, f"Текущая температура: {temperature[0]}°C\nВлажность: {humidity[1]}%\nДавление: {pressure[2]} мм.рт.ст\nВетер: {wind[3]} м/с")
    bot.send_message(message.chat.id, "Введите название города, чтобы продолжить")
    bot.register_next_step_handler(msg, print_weather)
bot.polling()
