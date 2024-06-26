import pymongo
from datetime import datetime

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Notion"]
collection = db["notion_subscriptions"]


def save_user_data(user_id, email, start_date, end_date, subscription_status="inactive", subscription_type="free"):
    user_data = {
        "user_id": user_id,
        "email": email,
        "start_date": start_date,
        "end_date": end_date,
        "subscription_status": subscription_status,
        "subscription_type": subscription_type
    }
    return collection.insert_one(user_data)


def update_user_data(user_id, email=None, start_date=None, end_date=None, subscription_status=None,
                     subscription_type=None):
    update_data = {}
    if email:
        update_data["email"] = email
    if start_date:
        update_data["start_date"] = datetime.strptime(start_date, "%Y-%m-%d")
    if end_date:
        update_data["end_date"] = datetime.strptime(end_date, "%Y-%m-%d")
    if subscription_status:
        update_data["subscription_status"] = subscription_status
    if subscription_type:
        update_data["subscription_type"] = subscription_type

    collection.update_one({"user_id": user_id}, {"$set": update_data})


def get_user_data(user_id):
    user_data = collection.find_one({"user_id": user_id})
    return user_data


async def print_user_data(user_id, message):
    user_data = get_user_data(user_id)
    if user_data:
        response = f"ID Користувача: {user_data['user_id']}\n"
        response += f"Електронна пошта: {user_data['email']}\n"

        if isinstance(user_data['start_date'], str) and user_data['start_date']:
            user_data['start_date'] = datetime.strptime(user_data['start_date'], '%Y-%m-%d')

        if isinstance(user_data['end_date'], str) and user_data['end_date']:
            user_data['end_date'] = datetime.strptime(user_data['end_date'], '%Y-%m-%d')

        response += f"Дата початку: {user_data['start_date'].strftime('%Y-%m-%d') if user_data['start_date'] else ''}\n"
        response += f"Дата закінчення: {user_data['end_date'].strftime('%Y-%m-%d') if user_data['end_date'] else ''}\n"
        response += f"Статус підписки: {user_data['subscription_status']}\n"
        response += f"Тип підписки: {user_data['subscription_type']}"
        await message.answer(response)
    else:
        await message.answer("Користувач с таким ID не знайден.")


def get_user_email(user_id):
    fields = {"email": 1}
    user_data = collection.find_one({"user_id": user_id}, fields)
    if user_data:
        return user_data.get('email')
    else:
        return None
