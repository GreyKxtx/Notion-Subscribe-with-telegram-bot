import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from gmail.email_processor import EmailProcessor

def initiate_chrome():
    options = Options()
    options.add_argument("--disable-infobars")
    options.add_argument("start-maximized")
    options.add_argument("--disable-extensions")
    options.add_experimental_option(
        "prefs", {
            "profile.default_content_setting_values.notifications": 1
        }
    )
    return webdriver.Chrome(options=options)

# Инициализация браузера
driver = initiate_chrome()

# Переход на страницу входа
driver.get("https://www.notion.so/login")

# Ожидание появления поля ввода с помощью явного ожидания
wait = WebDriverWait(driver, 10)  # Максимальное время ожидания - 10 секунд
email_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#notion-email-input-2')))

# Ввод адреса электронной почты
email_input.send_keys("andreykorsun1312@gmail.com")

# Находим кнопку "Continue" по атрибуту role или XPath и нажимаем на нее
continue_button = driver.find_element(By.XPATH, "//*[@id='notion-app']/div/div[1]/div/main/div[1]/section/div/div/div/div[2]/div[1]/div[3]/form/div[4]")
continue_button.click()

# Ожидание появления поля для ввода кода
code_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Paste login code"]')))

time.sleep(5)
# Получение кода из почты
email_processor = EmailProcessor('andreykorsun1312@gmail.com', 'hdwq mocn wjiv zdbr')
code = email_processor.process_email('notify@mail.notion.so')


# Ввод кода
code_input.send_keys(code)

# Нажатие кнопки "Continue" после ввода кода
continue_with_login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#notion-app > div > div:nth-child(1) > div > main > div:nth-child(1) > section > div > div > div > div.notion-login > div:nth-child(1) > div:nth-child(3) > form > div:nth-child(7)')))
continue_with_login_button.click()

# Ожидание сообщения об ошибке
error_message = None
try:
    error_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#notion-app > div > div:nth-child(1) > div > main > div:nth-child(1) > section > div > div > div > div.notion-login > div:nth-child(1) > div:nth-child(3) > div')))
except:
    pass

if error_message is not None and "Your login code was incorrect. Please try again." in error_message.text:
    print("Ошибка: Неправильный код")
    # Если выбивает ошибку "Неправильный код", повторно получаем код из почты и вводим его
    code = email_processor.process_email('notify@mail.notion.so')
    code_input.clear()  # Очищаем поле ввода кода
    code_input.send_keys(code)  # Вводим новый код
    continue_with_login_button.click()  # Нажимаем кнопку "Continue" снова

# Удаление




settings_members_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Settings & members")]')))
settings_members_button.click()

time.sleep(5)

# Найти элемент по тексту "Guests" и нажать на него
guests_element = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Guests")]')))
guests_element.click()

time.sleep(2)



# Найти все строки (tr) в таблице
rows = driver.find_elements(By.XPATH, '//table//tbody//tr')

for row in rows:
    print(row.text)  # Вывести текст строки (для отладки)
    # Найти ячейку (td) с адресом электронной почты в первом столбце
    email_cell = None
    try:
        email_cell = WebDriverWait(row, 3).until(
            EC.visibility_of_element_located((By.XPATH, './/td[1]//div[contains(text(),"max.exit.off@gmail.com")]'))
        )
    except:
        continue
    # Если найдена ячейка с нужной почтой
    if email_cell:

        # Найти кнопку "ellipsis" в третьем столбце (td) этой строки
        ellipsis_button = None
        try:
            ellipsis_button = WebDriverWait(row, 3).until(
                EC.visibility_of_element_located((By.XPATH, './/td[3]//div[contains(@role, "button")]'))
            )
        except:
            continue
        # Если кнопка найдена, выполнить необходимые действия с ней
        if ellipsis_button:
            # Нажать на кнопку "ellipsis"
            ellipsis_button.click()
            # Добавим ожидание перед поиском кнопки "Remove from workspace"
            time.sleep(3)
            # Найти кнопку "Remove from workspace"
            try:
                remove_from_workspace_button = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, '//div[text()="Remove from workspace"]'))
                )
                remove_from_workspace_button.click()
                time.sleep(1)
            except:
                continue
            remove_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Remove"]')))
            remove_button.click()
            time.sleep(1)
            break  # Прервать цикл после первой найденной кнопки

# Подождать некоторое время после нажатия на кнопку (для демонстрации)
time.sleep(2)



driver.quit()
