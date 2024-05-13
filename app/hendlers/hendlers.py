from datetime import datetime, timedelta

from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards.replay_keyboards as rkb
import app.keyboards.inline_keyboard as ikb
import app.database.db as db
from app.database.db import print_user_data

from app.notion.notion import Notion

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    user_id = message.from_user.id
    existing_user = db.collection.find_one({"user_id": user_id})

    if existing_user:
        await message.answer('Вітаемо! Ваш аккаунт вже створенний.', reply_markup=rkb.main)
    else:
        # Создаем аккаунт пользователя в базе данных с дополнительными полями
        db.save_user_data(
            user_id=user_id,
            email="",
            start_date=None,
            end_date=None,
            subscription_status="inactive",
            subscription_type=""
        )

        await message.answer('Вітаемо! Ваш аккаунт створен успішно.', reply_markup=rkb.main)


class Register(StatesGroup):
    gmail = State()


@router.message(Command("login"))
async def register(message: Message, state: FSMContext):
    await state.set_state(Register.gmail)
    await message.answer('Для авторизації введіть пошту яка зареестрована на Notion', reply_markup=rkb.main)


@router.message(Register.gmail)
async def register_gmail(message: Message, state: FSMContext):
    await state.update_data(gmail=message.text)
    data = await state.get_data()
    user_id = message.from_user.id
    await message.answer(f'Почта {data["gmail"]} зарегестрированна ')
    db.update_user_data(
        user_id=user_id,
        email=data['gmail'],  # Здесь можно добавить дополнительные данные, если они необходимы
        start_date="",  # Здесь можно добавить дополнительные данные, если они необходимы
        end_date="",  # Здесь можно добавить дополнительные данные, если они необходимы
    )

    await state.clear()


@router.message(F.text == "Обліковий запис")
async def account(message: Message):
    user_id = message.from_user.id
    await print_user_data(user_id, message)


@router.message(F.text == "Підписки")
async def subscribe(message: Message):
    await message.answer("Оберить підписку на Workspace на Notion", reply_markup=ikb.catalog)


@router.message(F.text == "Про нас")
async def about(message: Message):
    await message.answer(
        "Ласкаво просимо до нашого бота! Ми раді бачити вас тут. Тут ви можете здійснювати та керувати вашими підписками на Notion зручним для вас способом."
        "\n\nПідписки:\nУ розділі \"Підписки\" ви можете оформити підписку на цікаві для вас теми в Notion. Просто вкажіть тему, яка вас цікавить, і ми надамо вам доступ до відповідних ресурсів."
        "\n\nОбліковий запис:\nУ розділі \"Обліковий запис\" ви можете переглянути інформацію про свій обліковий запис. Тут ви знайдете інформацію про ваш тип підписки, дати початку та завершення, а також стан вашого облікового запису."
        "\n\nМи працюємо для того, щоб зробити ваше користування нашим сервісом якнайзручнішим та продуктивним. Не соромтеся звертатися до нас з будь-якими питаннями або запитами. Дякуємо, що обрали нас!")


# route для InlineKeyboardMarkup
@router.callback_query(F.data == "1_Month")
async def subscribe(callback: CallbackQuery):
    user_id = callback.from_user.id
    gmail = db.get_user_email(user_id)

    # Отправляем сообщение о начале процесса приглашения
    invite_message = await callback.message.answer("Виконується запрошення в Notion...")
    await callback.answer('')
    try:
        # Проводим приглашение в Notion
        notion = Notion()
        notion.login()
        notion.invite_to_workspace(gmail)

        # Заменяем сообщение о процессе приглашения на сообщение об успешном приглашении
        await invite_message.edit_text("Запрошення надіслано успішно!")

        current_date = datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(seconds=30)).strftime("%Y-%m-%d")

        db.update_user_data(user_id=user_id, start_date=current_date, end_date=end_date, subscription_status="Активна",
                            subscription_type="1 Місяць")

    except Exception as e:
        # В случае возникновения ошибки выводим сообщение об ошибке
        print(f"Произошла ошибка при приглашении: {str(e)}")
