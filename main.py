from telebot import types
import telebot
from parse import get_category, request_id
from tokens import bot_token

bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    main_button = types.KeyboardButton("Courses")
    markup.add(main_button)
    bot.send_message(message.chat.id, "Hi!", reply_markup=markup)

    bot.register_next_step_handler(message, return_categories)


categories_and_courses = get_category()
courses = []


@bot.message_handler()
def return_categories(message):
    if message.text == "Courses":
        markup = types.ReplyKeyboardMarkup()
        for i in categories_and_courses:
            markup.add(types.KeyboardButton(i[0]))

        bot.send_message(message.chat.id, "Choose courses category: ", reply_markup=markup)

        bot.register_next_step_handler(message, return_courses_names)


@bot.message_handler()
def return_courses_names(message):
    markup = types.ReplyKeyboardMarkup()
    for i in categories_and_courses:
        if message.text == i[0]:
            courses_id = i[1]
            for j in courses_id:
                course_name = request_id(j)
                courses.append([course_name, "https://stepik.org/course/" + str(j)])
                markup.add(types.KeyboardButton(course_name))
    bot.send_message(message.chat.id, "Choose liked course: ", reply_markup=markup)
    bot.register_next_step_handler(message, return_links)


@bot.message_handler()
def return_links(message):
    c = 1
    for i in courses:
        if message.text == i[0]:
            bot.reply_to(message, f"Link on this course: \n  {i[1]}")
            c = 0
    if c:
        bot.reply_to(message, "Can't find this course")
    bot.register_next_step_handler(message, return_links)


bot.infinity_polling(none_stop=True)