import os
import sys
import requests

import dotenv
from pathlib import Path

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

dotenv_path = Path('.') / '.env'
dotenv.load_dotenv(dotenv_path)

if len(sys.argv) < 4:
    print("Usage: python main.py <query> <location> <salary>")
    exit(1)

query = sys.argv[1]
location = sys.argv[2]
salary = sys.argv[3]

is_notify_telegram = os.getenv("NOTIFY_TELEGRAM", "False")
is_notify_discord = os.getenv("NOTIFY_DISCORD", "False")

# Example Page https://nodeflair.com/jobs?query=DevOps&page=1&sort_by=relevant&countries%5B%5D=Singapore&salary_min=8000

URL = f"https://nodeflair.com/jobs?query={query}&page=1&sort_by=relevant&countries%5B%5D={location}&salary_min={salary}"

# Set headless mode
options = Options()
options.add_argument("-headless")
browser = Firefox(options=options)

browser.get(URL)

try:
    xpath = "/html/body/div[4]/div[2]/div[4]/div[1]"
    h2s = browser.find_elements(By.XPATH, f"{xpath}//h2")
    wait = WebDriverWait(browser, 3)
    h2s = wait.until(EC.presence_of_all_elements_located((By.XPATH, f"{xpath}//h2")))

    roles = []
    for i in range(len(h2s)):
        role = h2s[i].text
        roles.append(role)

    salaries = []
    companies = []

    links = browser.find_elements(By.XPATH, f"{xpath}//a")
    wait = WebDriverWait(browser, 3)
    links = wait.until(EC.presence_of_all_elements_located((By.XPATH, f"{xpath}//a")))
    detail_links = []

    # get first 12 links only
    for i in range(12):
        link = links[i].get_attribute("href")
        detail_links.append(link)

    rating_salaries_companies = browser.find_elements(By.XPATH, f"{xpath}//p/span")
    wait = WebDriverWait(browser, 3)
    rating_salaries_companies = wait.until(
        EC.presence_of_all_elements_located((By.XPATH, f"{xpath}//p/span"))
    )

    for i in range(len(rating_salaries_companies)):
        d = rating_salaries_companies[i].text.strip()

        if d == "EST" or d[0].isdigit():
            continue

        if d.startswith("S$"):
            salaries.append(d)
            continue

        if d[0].isalpha():
            companies.append(d)
            continue

    for i in range(len(roles)):
        message = f"{roles[i]}\n {salaries[i]}\n {companies[i]}\n {detail_links[i]}"

        if is_notify_telegram and is_notify_telegram != "False":
            print("Sending Telegram notification")
            telegram_webhook = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
            chat_id = os.getenv("CHAT_ID")

            print(f"Telegram webhook: {telegram_webhook}")
            print(f"Chat ID: {chat_id}")


            requests.post(telegram_webhook, data={
                          "chat_id": chat_id, "text": message})

        if is_notify_discord:
            print("Sending Discord notification")
            discord_webhook = os.getenv("DISCORD_WEBHOOK")
            
            message = f"{message}\n---"
            requests.post(discord_webhook, json={"content": message})

        print(message)

except:
    print("No results found")
    # print error
    print(sys.exc_info()[0])

browser.quit()