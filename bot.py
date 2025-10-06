import telebot
import openai
import os

# Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# Пайдаланушы /topic <тема> деп жібергенде сұрақ жасау
@bot.message_handler(commands=['topic'])
def topic_handler(message):
    topic = message.text.replace('/topic ', '')  # /topic матнінен тақырып алу

    # OpenAI GPT арқылы сұрақ жасау
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # gpt-4 орнына
        messages=[{"role": "user", "content": f"{topic} тақырыбында 5 сұрақ жаса"}]
    )

    # GPT жауабын шығарып алу
    quiz_text = response['choices'][0]['message']['content']

    # Telegram-ға жіберу
    bot.send_message(message.chat.id, quiz_text)

# Ботты іске қосу
bot.polling()
