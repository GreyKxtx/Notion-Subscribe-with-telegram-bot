import imaplib
import email
import re
import base64

class EmailProcessor:
    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password

    def process_email(self, sender):
        try:
            # Подключение к серверу IMAP Gmail
            imap_conn = imaplib.IMAP4_SSL('imap.gmail.com')
            imap_conn.login(self.email_address, self.password)

            # Выбор папки "INBOX"
            imap_conn.select('INBOX')

            # Поиск всех сообщений от указанного отправителя
            status, email_ids = imap_conn.search(None, '(FROM "{}")'.format(sender))
            email_ids = email_ids[0].split()

            # Проходимся по всем сообщениям, начиная с самого нового
            for email_id in reversed(email_ids):
                # Получение заголовка и тела текущего сообщения
                status, email_data = imap_conn.fetch(email_id, '(RFC822)')
                raw_email = email_data[0][1]
                msg = email.message_from_bytes(raw_email)

                # Получение заголовка сообщения
                subject = msg["Subject"]

                # Раскодируем заголовок сообщения, если он закодирован в формате base64
                if subject.startswith('=?UTF-8?B?'):
                    subject = base64.b64decode(subject[10:-2]).decode('utf-8')

                # Проверяем, содержит ли заголовок сообщения интересующую нас фразу
                if "Your temporary Notion login code is" in subject:

                    # Ищем код в заголовке сообщения
                    code_match = re.search(r'Your temporary Notion login code is ([\w-]+)', subject)
                    if code_match:
                        code = code_match.group(1)
                        imap_conn.logout()
                        return code  # Возвращаем код, если он найден

            imap_conn.logout()
            return None  # Возвращаем None, если код не найден

        except Exception as e:
            print("Произошла ошибка:", e)
            return None  # Возвращаем None в случае ошибки

# Пример использования:
email_processor = EmailProcessor('andreykorsun1312@gmail.com', 'hdwq mocn wjiv zdbr')
code = email_processor.process_email('notify@mail.notion.so')

