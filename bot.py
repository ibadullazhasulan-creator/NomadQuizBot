import telebot

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Сәлем! Мен Nomad Quiz ботымын 🤖")

@bot.message_handler(commands=['quiz'])
def quiz(message):
    question = "Қазақстанның астанасы қай қала?"
    options = ["Алматы", "Астана", "Шымкент", "Қызылорда"]
    bot.send_poll(message.chat.id, question, options, type='quiz', correct_option_id=1)

bot.polling()
