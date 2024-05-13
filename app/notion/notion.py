import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .gmail_func.email_processor import EmailProcessor

class Notion:
    def __init__(self, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")  # Запустити у режимі безголовного виконання
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        self.email_processor = EmailProcessor('andreykorsun1312@gmail.com', 'hdwq mocn wjiv zdbr')

    def login(self):
        self.driver.get("https://www.notion.so/login")
        email_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#notion-email-input-2')))
        email_input.send_keys("andreykorsun1312@gmail.com")
        continue_button = self.driver.find_element(By.XPATH, "//*[@id='notion-app']/div/div[1]/div/main/div[1]/section/div/div/div/div[2]/div[1]/div[3]/form/div[4]")
        continue_button.click()
        code_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[placeholder="Paste login code"]')))
        time.sleep(5)
        code = self.email_processor.process_email('notify@mail.notion.so')
        code_input.send_keys(code)
        continue_with_login_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#notion-app > div > div:nth-child(1) > div > main > div:nth-child(1) > section > div > div > div > div.notion-login > div:nth-child(1) > div:nth-child(3) > form > div:nth-child(7)')))
        continue_with_login_button.click()

    def invite_to_workspace(self, email):
        share_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.notion-topbar-share-menu')))
        share_button.click()
        time.sleep(3)
        share_email_input = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]')))
        share_email_input.send_keys(email)
        time.sleep(3)
        invite_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="notion-app"]/div/div[2]/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/div[2]/div[1]/div/div[2]')))
        invite_button.click()
        time.sleep(2)

    def remove_from_workspace(self, email):
        settings_members_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Settings & members")]')))
        settings_members_button.click()
        time.sleep(3)
        guests_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(text(), "Guests")]')))
        guests_element.click()
        time.sleep(2)

        # Найти все строки (tr) в таблице
        rows = self.driver.find_elements(By.XPATH, '//table//tbody//tr')

        for row in rows:
            # Найти ячейку (td) з адресом електронної пошти в першому стовпці
            email_cell = None
            try:
                email_cell = WebDriverWait(row, 3).until(
                    EC.visibility_of_element_located((By.XPATH, f'.//td[1]//div[contains(text(),"{email}")]'))
                )
            except:
                continue
            # Якщо знайдена комірка з потрібною поштою
            if email_cell:

                # Найти кнопку "ellipsis" у третьому стовпці (td) цього рядка
                ellipsis_button = None
                try:
                    ellipsis_button = WebDriverWait(row, 3).until(
                        EC.visibility_of_element_located((By.XPATH, './/td[3]//div[contains(@role, "button")]'))
                    )
                except:
                    continue
                # Якщо кнопка знайдена, виконати необхідні дії з нею
                if ellipsis_button:
                    # Натиснути на кнопку "ellipsis"
                    ellipsis_button.click()
                    # Додамо очікування перед пошуком кнопки "Remove from workspace"
                    time.sleep(3)
                    # Знайти кнопку "Remove from workspace"
                    try:
                        remove_from_workspace_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, '//div[text()="Remove from workspace"]'))
                        )
                        remove_from_workspace_button.click()
                        time.sleep(1)
                    except:
                        continue
                    remove_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[text()="Remove"]')))
                    remove_button.click()
                    time.sleep(1)
                    break  # Перервати цикл після першої знайденої кнопки

        # Почекати деякий час після натискання на кнопку (для демонстрації)
        time.sleep(2)

    def close_browser(self):
        self.driver.quit()

# Використання класу
#notion_bot = Notion()  # Запуск у режимі безголовного виконання
#notion_bot.login()
#notion_bot.invite_to_workspace("andreykorsun51@gmail.com")
#notion_bot.remove_from_workspace("max.exit.off@gmail.com")
#notion_bot.close_browser()
