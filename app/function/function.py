from datetime import datetime
from app.database.db import collection, db
from app.notion.notion import Notion


async def remove_expired_users():
    while True:

        print("Крон задача запущена")
        current_date = datetime.now()

        expired_users = collection.find({"end_date": {"$lt": current_date}})

        # Проходимся по каждому пользователю с истекшей подпиской
        for user in expired_users:
            # Получаем ID пользователя и его электронную почту
            user_id = user["user_id"]
            email = user["email"]

            notion_bot = Notion()  # Запуск в режиме безголового выполнения
            notion_bot.login()
            notion_bot.remove_from_workspace(email)  # Передаем переменную email, а не строку "email"
            notion_bot.close_browser()

            # Обновляем информацию о пользователе
            db.update_user_data(user_id=user_id, start_date="", end_date="", subscription_status="Закінчилася",
                                subscription_type="")

    await asyncio.sleep(30)
    print("Функция remove_expired_users отработала")
