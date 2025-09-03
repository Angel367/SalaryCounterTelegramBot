import telebot
from telebot import types
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Получение данных из .env
BOT_TOKEN = os.getenv('BOT_TOKEN')
MY_SALARY = float(os.getenv('MY_SALARY'))
PARTNER_SALARY = float(os.getenv('PARTNER_SALARY'))

# Проверка обязательных переменных
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не установлен в .env файле")

bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_calc = types.KeyboardButton('💵 Рассчитать взносы')
    item_info = types.KeyboardButton('📊 Текущие настройки')
    markup.add(item_calc, item_info)

    bot.send_message(
        message.chat.id,
        f"👋 Привет! Я бот для расчета взносов по зарплатам.\n"
        f"📈 Текущие зарплаты:\n"
        f"• Егоричек: {format_number(MY_SALARY)} ₽\n"
        f"• Линчичек: {format_number(PARTNER_SALARY)} ₽\n\n"
        "Нажмите '💵 Рассчитать взносы' чтобы начать расчет.",
        reply_markup=markup,
        parse_mode='Markdown'
    )


@bot.message_handler(func=lambda message: message.text == '📊 Текущие настройки')
def show_settings(message):
    total_income = MY_SALARY + PARTNER_SALARY
    my_share = MY_SALARY / total_income
    partner_share = PARTNER_SALARY / total_income

    bot.send_message(
        message.chat.id,
        f"⚙️ *Текущие настройки:*\n\n"
        f"• Егоричек: `{format_number(MY_SALARY)}` ₽\n"
        f"• Линчичек: `{format_number(PARTNER_SALARY)}` ₽\n"
        f"• Общий доход: `{format_number(total_income)}` ₽\n"
        f"• Егоричека доля: {my_share:.1%}\n"
        f"• Линчичека доля: {partner_share:.1%}",
        parse_mode='Markdown'
    )


@bot.message_handler(func=lambda message: message.text == '💵 Рассчитать взносы')
def ask_amount(message):
    msg = bot.send_message(message.chat.id, "💶 Введите общую сумму, которую нужно собрать (руб):")
    bot.register_next_step_handler(msg, process_amount_step)


def process_amount_step(message):
    try:
        amount = float(message.text.replace(' ', '').replace(',', '.'))

        if amount <= 0:
            bot.send_message(message.chat.id, "❌ Сумма должна быть больше 0!")
            return

        calculate_contributions(message, amount)

    except ValueError:
        bot.send_message(message.chat.id, "❌ Пожалуйста, введите число!")


def calculate_contributions(message, amount):
    # Расчет пропорций
    total_income = MY_SALARY + PARTNER_SALARY
    my_share = MY_SALARY / total_income
    partner_share = PARTNER_SALARY / total_income

    my_contribution = amount * my_share
    partner_contribution = amount * partner_share

    # Создание ответа
    result_text = f"""
💡 *Результаты расчета:*

• Егоричкова зарплата: `{format_number(MY_SALARY)}` ₽
• Линчикова зарплата: `{format_number(PARTNER_SALARY)}` ₽
• Общая сумма: `{format_number(amount)}` ₽

📊 *Пропорции:*
• Егорикова доля: {my_share:.1%}
• Линчикова доля: {partner_share:.1%}

💵 *Взносы:*
• Егориков взнос: `{format_number(my_contribution)}` ₽
• Линчиков взнос: `{format_number(partner_contribution)}` ₽

✅ *Проверка:* `{format_number(my_contribution + partner_contribution)}` ₽
"""

    bot.send_message(message.chat.id, result_text, parse_mode='Markdown')


def format_number(num):
    """Форматирование чисел с пробелами и запятой"""
    return f"{num:,.2f}".replace(',', ' ').replace('.', ',')


@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if message.text not in ['💵 Рассчитать взносы', '📊 Текущие настройки']:
        bot.send_message(
            message.chat.id,
            "Используйте кнопки меню или команды:\n"
            "/start - начать работу\n"
            "/help - помощь"
        )


if __name__ == '__main__':
    print("=" * 50)
    print("Бот запущен с настройками:")
    print(f"• Егорикова зарплата: {format_number(MY_SALARY)} ₽")
    print(f"• Линчикова зарплата: {format_number(PARTNER_SALARY)} ₽")
    print(f"• Общий доход: {format_number(MY_SALARY + PARTNER_SALARY)} ₽")
    print("=" * 50)

    print("Бот запущен...")
    bot.infinity_polling()