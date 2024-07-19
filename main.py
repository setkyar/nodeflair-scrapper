import os
import sys
import requests
import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Load environment variables
dotenv_path = Path('.') / '.env'
load_dotenv(dotenv_path)

# Check command-line arguments
if len(sys.argv) < 4:
    print("Usage: python main.py <query> <location> <salary>")
    sys.exit(1)

query = sys.argv[1]
location = sys.argv[2]
salary = sys.argv[3]

is_notify_telegram = os.getenv("NOTIFY_TELEGRAM", "False") == "True"
is_notify_discord = os.getenv("NOTIFY_DISCORD", "False") == "True"

# Construct URL
URL = f"https://nodeflair.com/jobs?query={query}&page=1&sort_by=relevant&countries%5B%5D={location}&salary_min={salary}"

# Set headless mode
options = Options()
options.add_argument("-headless")
browser = webdriver.Firefox(options=options)

try:
    browser.get(URL)

    # Wait until elements are located
    xpath = "/html/body/div[4]/div[2]/div[4]/div[1]"
    wait = WebDriverWait(browser, 10)
    h2s = wait.until(EC.presence_of_all_elements_located((By.XPATH, f"{xpath}//h2")))

    roles = [h2.text for h2 in h2s]

    links = browser.find_elements(By.XPATH, f"{xpath}//a")
    detail_links = [link.get_attribute("href") for link in links[:12]]

    rating_salaries_companies = browser.find_elements(By.XPATH, f"{xpath}//p/span")
    data = [elem.text.strip() for elem in rating_salaries_companies]

    salaries = [d for d in data if d.startswith("S$")]
    companies = [d for d in data if not d.startswith("S$") and d[0].isalpha()]

    min_length = min(len(roles), len(salaries), len(companies), len(detail_links))

    for i in range(min_length):
        message = f"{roles[i]}\n{salaries[i]}\n{companies[i]}\n{detail_links[i]}"

        if is_notify_telegram:
            print("Sending Telegram notification")
            telegram_webhook = f"https://api.telegram.org/bot{os.getenv('TELEGRAM_BOT_TOKEN')}/sendMessage"
            chat_id = os.getenv("CHAT_ID")
            requests.post(telegram_webhook, data={"chat_id": chat_id, "text": message})

        if is_notify_discord:
            print("Sending Discord notification")
            discord_webhook = os.getenv("DISCORD_WEBHOOK")
            requests.post(discord_webhook, json={"content": message})

        print(message)

except Exception as e:
    print("No results found")
    print(f"Error: {e}")

finally:
    browser.quit()

