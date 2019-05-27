from telebot import types


def start_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('🏪 АТБ'))
    markup.row(types.KeyboardButton('🔍 Поиск товара'))

    return markup


def get_atb_discounts_preview_menu(size, page):
    if size > 9:
        raise IndexError
    markup = types.InlineKeyboardMarkup(row_width=size)
    temp = []
    for i in range(size):
        temp.append(types.InlineKeyboardButton('{}'.format(i + 1),
                                               callback_data='atb_discounts_preview_{}_{}_{}'.format(i, size, page)))
    markup.add(*temp)
    markup.add(types.InlineKeyboardButton('◀️', callback_data='atb_discounts_preview_page_{}_{}'.format(size, page - 1)),
               types.InlineKeyboardButton('▶️', callback_data='atb_discounts_preview_page_{}_{}'.format(size, page + 1)))

    return markup


def get_atb_discounts_menu(page):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('◀️', callback_data='atb_discounts_{}'.format(page - 1)),
               types.InlineKeyboardButton('▶️', callback_data='atb_discounts_{}'.format(page + 1)))
    markup.add(types.InlineKeyboardButton('↩️ К превью', callback_data='atb_discounts_back_{}'.format(page)))

    return markup