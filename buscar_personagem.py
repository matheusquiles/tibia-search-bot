import requests
import os
from bs4 import BeautifulSoup

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

URL = "https://www.tibia.com/charactertrade/?subtopic=currentcharactertrades"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
}

resultados = []

# =========================
# LOOP DE BUSCA
# =========================
for personagem in PERSONAGENS:
    payload = {
        "searchstring": personagem
    }

    response = requests.post(URL, headers=HEADERS, data=payload, timeout=30)

    soup = BeautifulSoup(response.text, "html.parser")

    if soup.find("td", string="No character auctions found."):
        resultados.append(f"❌ {personagem}: não encontrado")
    else:
        resultados.append(f"✅ {personagem}: encontrado")

# =========================
# RESULTADO FINAL
# =========================
mensagem_final = "📊 Resultado da busca diária:\n\n" + "\n".join(resultados)
print(mensagem_final)
enviar_telegram(mensagem_final)
