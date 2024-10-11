import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from secret import *
from connection import *
bot = telebot.TeleBot(api_key)
create_tables()

def add_car(brand, model, year):
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(
        "insert into cars (brand, model, year) values (%(brand)s, %(model)s, %(year)s)",
        {'brand': brand, 'model': model, 'year': year}
    )
    conn.commit()
    close_connection(conn, cur)

def get_all_cars():
    conn = open_connection()
    cur = conn.cursor()
    cur.execute("select * from cars")
    cars = cur.fetchall()
    close_connection(conn, cur)
    return cars

def get_car_by_id(car_id):
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(
        "select *from cars where car_id = %(car_id)s",
        {'car_id': car_id}
    )
    car = cur.fetchone()
    close_connection(conn, cur)
    return car

def update_car(car_id, brand, model, year):
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(
        "update cars set brand = %(brand)s, model = %(model)s, year = %(year)s where car_id = %(car_id)s",
        {'brand': brand, 'model': model, 'year': year, 'car_id': car_id}
    )
    conn.commit()
    close_connection(conn, cur)

def delete_car(car_id):
    conn = open_connection()
    cur = conn.cursor()
    cur.execute(
        "delete from cars where car_id = %(car_id)s",
        {'car_id': car_id}
    )
    conn.commit()
    close_connection(conn, cur)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Add car 🚘"))
    markup.add(KeyboardButton("Update car 🔧"))
    markup.add(KeyboardButton("Show all cars 👀"))
    markup.add(KeyboardButton("Find car by ID 🔎"))
    markup.add(KeyboardButton("Delete car 🛒"))
    bot.send_message(message.chat.id, "Welcome to CarBot! Please choose an action:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Add car 🚘")
def add_car_step1(message):
    bot.send_message(message.chat.id, "Enter car brand: ")
    bot.register_next_step_handler(message, add_car_step2)

def add_car_step2(message):
    brand = message.text
    bot.send_message(message.chat.id, "Enter car model: ")
    bot.register_next_step_handler(message, add_car_step3, brand)

def add_car_step3(message, brand):
    model = message.text
    bot.send_message(message.chat.id, "Enter car year: ")
    bot.register_next_step_handler(message, add_car_step4, brand, model)

def add_car_step4(message, brand, model):
    try:
        year = int(message.text)
        add_car(brand, model, year)
        bot.send_message(message.chat.id, "Car successfully added!")
    except ValueError:
        bot.send_message(message.chat.id, "Please enter a valid year.")

@bot.message_handler(func=lambda message: message.text == "Show all cars 👀")
def show_cars(message):
    cars = get_all_cars()
    if cars:
        for car in cars:
            bot.send_message(message.chat.id, f"ID: {car[0]}, Brand: {car[1]}, Model: {car[2]}, Year: {car[3]}")
    else:
        bot.send_message(message.chat.id, "No cars found.")

@bot.message_handler(func=lambda message: message.text == "Update car 🔧")
def update_car_step1(message):
    bot.send_message(message.chat.id, "Enter car ID to update: ")
    bot.register_next_step_handler(message, update_car_step2)

def update_car_step2(message):
    try:
        car_id = int(message.text)
        bot.send_message(message.chat.id, "Enter new brand: ")
        bot.register_next_step_handler(message, update_car_step3, car_id)
    except ValueError:
        bot.send_message(message.chat.id, "Please enter a valid ID.")

def update_car_step3(message, car_id):
    brand = message.text
    bot.send_message(message.chat.id, "Enter new model: ")
    bot.register_next_step_handler(message, update_car_step4, car_id, brand)

def update_car_step4(message, car_id, brand):
    model = message.text
    bot.send_message(message.chat.id, "Enter new year: ")
    bot.register_next_step_handler(message, update_car_step5, car_id, brand, model)

def update_car_step5(message, car_id, brand, model):
    try:
        year = int(message.text)
        update_car(car_id, brand, model, year)
        bot.send_message(message.chat.id, "Car information successfully updated!")
    except ValueError:
        bot.send_message(message.chat.id, "Please enter a valid year.")

@bot.message_handler(func=lambda message: message.text == "Delete car 🛒")
def delete_car_step1(message):
    bot.send_message(message.chat.id, "Enter car ID to delete: ")
    bot.register_next_step_handler(message, delete_car_step2)

def delete_car_step2(message):
    try:
        car_id = int(message.text)
        delete_car(car_id)
        bot.send_message(message.chat.id, "Car successfully deleted!")
    except ValueError:
        bot.send_message(message.chat.id, "Please enter a valid ID.")

@bot.message_handler(func=lambda message: message.text == "Find car by ID 🔎")
def find_car_by_id_step1(message):
    bot.send_message(message.chat.id, "Enter car ID to search: ")
    bot.register_next_step_handler(message, find_car_by_id_step2)

def find_car_by_id_step2(message):
    try:
        car_id = int(message.text)
        car = get_car_by_id(car_id)
        if car:
            bot.send_message(message.chat.id, f"ID: {car[0]}, Brand: {car[1]}, Model: {car[2]}, Year: {car[3]}")
        else:
            bot.send_message(message.chat.id, "Car with this ID not found.")
    except ValueError:
        bot.send_message(message.chat.id, "Please enter a valid ID.")

bot.infinity_polling()