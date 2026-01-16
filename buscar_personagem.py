import os
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def enviar_telegram(mensagem):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        return
    requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": mensagem},
        timeout=20
    )

PERSONAGEM = "Telescopio Refrator"

URL = "https://www.tibia.com/charactertrade/"

params = {
    "subtopic": "currentcharactertrades",
    "type": "character",
    "searchstring": PERSONAGEM
}

response = requests.get(
    URL,
    params=params,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

soup = BeautifulSoup(response.text, "html.parser")

no_result = soup.find(
    "td",
    string=lambda t: t and "No character auctions found." in t
)

has_auction = soup.find(
    "a",
    href=lambda h: h and "auctiondetails" in h
)

if no_result:
    resultado = f"❌ {PERSONAGEM}: não encontrado"
elif has_auction:
    resultado = f"✅ {PERSONAGEM}: encontrado"
else:
    resultado = f"⚠️ {PERSONAGEM}: resultado inconclusivo"

print(resultado)
enviar_telegram(resultado)
