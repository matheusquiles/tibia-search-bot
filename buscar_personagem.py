from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import time
import os
import requests

# =========================
# CHROME OPTIONS (CI SAFE)
# =========================
options = Options()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")
options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

wait = WebDriverWait(driver, 30)

# =========================
# TELEGRAM
# =========================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def enviar_telegram(mensagem: str):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        print("Token ou Chat ID não configurados")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": mensagem
    }
    requests.post(url, data=payload, timeout=20)

# =========================
# PERSONAGENS
# =========================
PERSONAGENS = [
    "Kashimiro",
    "Telescopio Refrator",
    "Only Dyziox"
]

# =========================
# ACESSA PÁGINA
# =========================
driver.get("https://www.tibia.com/charactertrade/?subtopic=currentcharactertrades")

# Garante DOM carregado
wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

# Força render do formulário
driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
time.sleep(3)

resultados = []

# =========================
# LOOP DE BUSCA
# =========================
for personagem in PERSONAGENS:
    try:
        # Campo de busca (ID -> fallback por classe)
        try:
            campo_busca = wait.until(
                EC.visibility_of_element_located((By.ID, "ItemInput"))
            )
        except:
            campo_busca = wait.until(
                EC.visibility_of_element_located((
                    By.XPATH,
                    "//input[contains(@class,'AuctionInputSearch')]"
                ))
            )

        campo_busca.clear()
        campo_busca.send_keys(personagem)

        # Checkbox (Include all worlds / similar)
        try:
            checkbox = driver.find_element(
                By.XPATH,
                "//form//input[@type='checkbox']"
            )
            if not checkbox.is_selected():
                checkbox.click()
        except:
            pass  # se não achar, segue

        # Botão Search
        botao_buscar = wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                "//input[@type='submit' and contains(@class,'BigButtonText')]"
            ))
        )
        botao_buscar.click()

        time.sleep(5)

        # Verifica resultado
        try:
            driver.find_element(
                By.XPATH,
                "//td[contains(text(),'No character auctions found')]"
            )
            resultados.append(f"❌ {personagem}: não encontrado")
        except:
            resultados.append(f"✅ {personagem}: encontrado")

        time.sleep(2)

    except Exception as e:
        resultados.append(f"⚠️ {personagem}: erro ao processar")
        print(f"Erro com {personagem}: {e}")

# =========================
# RESULTADO FINAL
# =========================
mensagem_final = "📊 Resultado da busca diária:\n\n" + "\n".join(resultados)
print(mensagem_final)
enviar_telegram(mensagem_final)

driver.quit()
