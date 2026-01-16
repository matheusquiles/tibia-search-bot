from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import time
import os
import requests

# ========================
# CONFIGURA CHROME HEADLESS
# ========================
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 15)

# ========================
# TELEGRAM
# ========================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def enviar_telegram(mensagem):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Token ou Chat ID não configurados")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem
    }
    requests.post(url, data=payload)

# ========================
# PERSONAGENS
# ========================
PERSONAGENS = [
    "Kashimiro",
    "Telescopio Refrator"
]

driver.get("https://www.tibia.com/charactertrade/?subtopic=currentcharactertrades")

resultados = []

for personagem in PERSONAGENS:
    campo_busca = wait.until(
        EC.presence_of_element_located((By.ID, "ItemInput"))
    )
    campo_busca.clear()
    campo_busca.send_keys(personagem)

    checkbox = driver.find_element(
        By.XPATH,
        "/html/body/div[3]/div[3]/div[3]/div[5]/div/div/div[3]/table/tbody/tr/td/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr/td/form/div[4]/span[3]/input"
    )
    if not checkbox.is_selected():
        checkbox.click()

    botao_buscar = driver.find_element(
        By.XPATH,
        '//*[@id="CharacterAuctionSearchBlock"]/div[1]/div/div/input'
    )
    botao_buscar.click()

    time.sleep(5)

    try:
        driver.find_element(
            By.XPATH,
            "//td[contains(text(), 'No character auctions found')]"
        )
        resultados.append(f"❌ {personagem}: não encontrado")
    except:
        resultados.append(f"✅ {personagem}: encontrado")

    time.sleep(2)

mensagem_final = "📊 Resultado da busca diária:\n\n" + "\n".join(resultados)
print(mensagem_final)
enviar_telegram(mensagem_final)

driver.quit()
