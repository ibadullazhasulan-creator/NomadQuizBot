import os
import telebot

# Render-дағы Environment Variables арқылы токен мен chat_id алу
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))  # CHAT_ID міндетті түрде integer болуы керек

# Telebot объектісін жасау
bot = telebot.TeleBot(BOT_TOKEN)

# Токен дұрыс па тексеру
try:
    me = bot.get_me()
    print("Бот дұрыс жұмыс істейді ✅", me)
except Exception as e:
    print("BOT_TOKEN дұрыс емес немесе желіде проблема:", e)
    exit(1)

# Хабарлама жіберу (міндетті емес, тек тест үшін)
try:
    bot.send_message(CHAT_ID, "Сәлем! Бот Render-да жұмыс істеп тұр.")
    print("Хабарлама жіберілді ✅")
except Exception as e:
    print("Хабарлама жіберу кезінде қате:", e)

# Ботты polling режимінде іске қосу
bot.polling()

