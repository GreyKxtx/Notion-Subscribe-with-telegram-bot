from aiogram.types import ReplyKeyboardMarkup , KeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Обліковий запис')],
                                     [KeyboardButton(text='Підписки')],
                                     [KeyboardButton(text='Про нас')]], resize_keyboard=True, input_field_placeholder='Оберіть пункт меню...')


