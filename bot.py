import telebot
import openai
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(commands=['topic'])
def topic_handler(message):
    topic = message.text.replace('/topic ', '')  # /topic <тема> → тақырып

    # OpenAI арқылы сұрақ жасау
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"{topic} тақырыбында 5 сұрақ жаса"}]
    )

    quiz_text = response['choices'][0]['message']['content']
    bot.send_message(message.chat.id, quiz_text)

bot.polling()

