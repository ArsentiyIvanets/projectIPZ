import telebot

from DiscountsBot.markups import *
from DiscountsBot.utils import *
from DiscountsBot.const import TOKEN
from discounts.atb_discounts import discounts


bot = telebot.TeleBot(TOKEN)

# TODO: change delete message + send message to edit message (the same types of keyboard are available)


@bot.message_handler(commands=['start'])
def start_messaging(message):
    bot.send_message(message.chat.id,
                     'Hello! Press a button below!',
                     reply_markup=start_menu())


@bot.message_handler(func=lambda message: message.text == '🏪 АТБ')
def get_atb_discounts_preview(message):
    res = discounts
    size, page = 5, 0
    text = create_list_for_preview(res, size, page)
    bot.send_message(message.chat.id,
                     text,
                     parse_mode='html',
                     reply_markup=get_atb_discounts_preview_menu(size, page))


@bot.callback_query_handler(func=lambda call: call.data[:22] == 'atb_discounts_preview_')
def control_atb_next_discount_preview(call):
    data = call.data.split('_')[3:]
    res = discounts
    length = len(res)
    number, page = calculate_params_for_list(int(data[1]), int(data[2]), length)
    if data[0] == 'page':
        text = create_list_for_preview(res, number, page)
        bot.edit_message_text(text,
                              call.message.chat.id,
                              call.message.message_id,
                              parse_mode='html',
                              reply_markup=get_atb_discounts_preview_menu(number, page))
    else:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        page = int(data[0]) + number * page
        bot.send_photo(call.message.chat.id,
                       photo=res[page][0],
                       caption='{}\n💵 <b>{}</b>'.format(res[page][1], res[page][2]),
                       parse_mode='html',
                       reply_markup=get_atb_discounts_menu(page))
    bot.answer_callback_query(call.id, text='')


@bot.callback_query_handler(func=lambda call: call.data[:14] == 'atb_discounts_')
def get_atb_discounts(call):
    data = call.data.split('_')[2:]
    res = discounts
    length = len(res)
    bot.delete_message(call.message.chat.id, call.message.message_id)
    if data[0] == 'back':
        size, page = get_back_to_list(int(data[1]), 5, length)
        text = create_list_for_preview(res, size, page)
        bot.send_message(call.message.chat.id,
                         text,
                         parse_mode='html',
                         reply_markup=get_atb_discounts_preview_menu(size, page))
    else:
        page = get_page_for_next_position(int(data[0]), length)
        bot.send_photo(call.message.chat.id,
                       photo=res[page][0],
                       caption='{}\n💵 <b>{}</b>'.format(res[page][1], res[page][2]),
                       parse_mode='html',
                       reply_markup=get_atb_discounts_menu(page))
    bot.answer_callback_query(call.id, text='')


@bot.message_handler(func=lambda message: message.text == '🔍 Поиск товара')
def search_by_name_start(message):
    msg = bot.send_message(message.chat.id,
                           'Введите ключевое слово для поиска:',
                           parse_mode='html',
                           reply_markup=start_menu())
    bot.register_next_step_handler(msg, get_key_to_search)


def get_key_to_search(message):
    res = discounts
    key = message.text
    res = find_position_by_name(res, key)
    size, page = get_back_to_list(0, 5, len(res))
    text = create_list_for_preview(res, size, page)
    bot.send_message(message.chat.id,
                     text,
                     parse_mode='html',
                     reply_markup=get_atb_discounts_preview_menu(size, page))


def main():
    bot.polling(none_stop=True, timeout=20)


# bot.delete_webhook()
if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=20)
