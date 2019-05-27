def create_list_for_preview(lst, number, page):
    s = ''
    for i in range(number):
        s += '<b>{})</b> {}\n 💵<b>{}</b>\n'.format(i + 1, lst[i + page * number][1], lst[i + page * number][2])

    return s[:-1]


def calculate_params_for_list(number, page, length):
    if page * number >= length:
        number, page = 5, 0
    elif length - page * number < number or page == -1:
        number = length % number
        page = (length - number) // number
    elif length % 5 < length - page * number < 5:
        page = number * page // 5
        number = 5

    return number, page


def get_back_to_list(number, size, length):
    if number / size >= length // size:
        size = length % size
        page = length // size - 1
    else:
        page = number // size

    return size, page


def get_page_for_next_position(page, length):
    if page >= length:
        page = 0
    elif page == -1:
        page = length - 1

    return page


def find_position_by_name(lst, key):
    res = []
    for i in lst:
        if key.lower() in i[1].lower():
            res.append(i)

    return res
