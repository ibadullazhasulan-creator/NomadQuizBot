import os
import telebot
import openai

# Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# Пайдаланушы сұрақтары мен жауаптары
quizzes = {}
user_state = {}

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
        "Сәлем! 🌟\n"
        "Сіз тақырып берсеңіз, мен сол бойынша викторина сұрақтарын жасаймын.\n"
        "Тақырыпты жазу үшін: /topic <тема>\n"
        "Викторинаны бастау үшін: /quiz")

# /topic – тақырып арқылы сұрақ жасау
@bot.message_handler(commands=['topic'])
def topic_handler(message):
    topic = message.text.replace("/topic", "").strip()
    if not topic:
        bot.send_message(message.chat.id, "Тақырыпты жазу керек! Мысалы: /topic Қазақстан тарихы")
        return

    bot.send_message(message.chat.id, f"{topic} тақырыбы бойынша сұрақтар жасалуда... ⏳")

    # GPT арқылы сұрақтар генерациясы
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": f"{topic} тақырыбында 5 викторина сұрағын жаса, жауаптарын қос."
        }]
    )

    text = response['choices'][0]['message']['content']

    # GPT-тен алынған мәтінді сұрақтар мен жауаптарға бөлу
    quizzes[message.chat.id] = parse_questions(text)
    bot.send_message(message.chat.id, "Сұрақтар дайын! /quiz деп теріп бастауға болады ✅")

# /quiz – викторинаны бастау
@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    if message.chat.id not in quizzes or not quizzes[message.chat.id]:
        bot.send_message(message.chat.id, "Сұрақтар жоқ 😔. Алдымен /topic командасын қолданыңыз.")
        return

    user_state[message.chat.id] = 0
    send_question(message.chat.id)

# Сұрақ жіберу функциясы
def send_question(chat_id):
    index = user_state[chat_id]
    user_quiz = quizzes[chat_id]
    if index < len(user_quiz):
        bot.send_message(chat_id, user_quiz[index]["question"])
    else:
        bot.send_message(chat_id, "Викторина аяқталды! 🎉")
        user_state.pop(chat_id)

# Пайдаланушы жауаптарын тексеру
@bot.message_handler(func=lambda m: True)
def check_answer(message):
    chat_id = message.chat.id
    if chat_id not in user_state:
        return

    index = user_state[chat_id]
    user_quiz = quizzes[chat_id]
    correct_answer = user_quiz[index]["answer"]

    if message.text.strip().lower() == correct_answer.lower():
        bot.reply_to(message, "Дұрыс! ✅")
    else:
        bot.reply_to(message, f"Қате 😔. Дұрыс жауап: {correct_answer}")

    user_state[chat_id] += 1
    send_question(chat_id)

# GPT-тен шыққан мәтінді сұрақ/жауапқа бөлу функциясы
def parse_questions(text):
    """
    Мысалы, GPT жауап береді:
    1. Сұрақ? Жауап: ...
    2. Сұрақ? Жауап: ...
    """
    result = []
    lines = text.split("\n")
    for line in lines:
        if "Жауап:" in line:
            parts = line.split("Жауап:")
            question = parts[0].strip()
            answer = parts[1].strip()
            result.append({"question": question, "answer": answer})
    return result

# Ботты іске қосу
bot.polling()

