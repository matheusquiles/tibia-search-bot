import os
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def enviar_telegram(mensagem):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(
        url,
        data={"chat_id": CHAT_ID, "text": mensagem},
        timeout=20
    )

PERSONAGENS = [
    "Kashimiro",
    "Telescopio Refrator",
    "Only Dyziox"
]

URL = "https://www.tibia.com/charactertrade/?subtopic=currentcharactertrades"

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
})

session.get(URL, timeout=30)

resultados = []

for personagem in PERSONAGENS:
    payload = {
        "subtopic": "currentcharactertrades",
        "currentpage": "1",
        "searchstring": personagem
    }

    response = session.post(URL, data=payload, timeout=30)
    soup = BeautifulSoup(response.text, "html.parser")

    no_result = soup.find(
    "td",
    string=lambda t: t and "No character auctions found" in t
    )

    auction_rows = soup.select("div.InnerTableContainer table tr")

    if no_result:
        resultados.append(f"❌ {personagem}: não encontrado")
    elif len(auction_rows) > 1:
        resultados.append(f"✅ {personagem}: encontrado ({len(auction_rows) - 1})")
    else:
        resultados.append(f"❌ {personagem}: não encontrado")

mensagem_final = "📊 Resultado da busca diária:\n\n" + "\n".join(resultados)
print(mensagem_final)
enviar_telegram(mensagem_final)
