from telebot import types

from games import Battle

def generate_field_keyboard(shoots):
    """letters = 'ABCDEFGHIJ'
    rows = [' '.join([f'{letter}{num + 1}' for num in range(10)]) for letter in letters]
    keyboard = []
    for row in rows:
        keyboard.append(row)
    return keyboard"""
    alphabet = "ABCDEFGHIJ"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for row in range(1, 11):
        row_buttons = []

        for col in range(10):
            cell_name = alphabet[col] + str(row)
            a = shoots[row-1][col]

            if a is None:
                btn_text = cell_name
            elif a:
                btn_text = "❌"  # Крестик в случае попадания
            else:
                btn_text = "⭕️"  # Круг в случае промаха

            row_buttons.append(btn_text)

        markup.row(*row_buttons)

    btn = types.KeyboardButton("Сдаться")
    markup.add(btn)
    return markup



