import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

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
BASE_URL = "https://www.tibia.com/charactertrade/"

params = {
    "subtopic": "currentcharactertrades",
    "searchstring": PERSONAGEM,
    "searchtype": "3",  # Força busca por "Character Name"
    # Params defaults do form (para simular busca completa)
    "currentpage": "1",
    "order_column": "101",
    "order_direction": "1",
    "filter_profession": "0",
    "filter_levelrangefrom": "",
    "filter_levelrangeto": "",
    "filter_world": "",
    "filter_worldpvptype": "9",  # Valor default no HTML, mas pode ajustar se precisar
    "filter_worldbattleyestate": "0",
    "filter_skillid": "",
    "filter_skillrangefrom": "",
    "filter_skillrangeto": ""
}

response = requests.get(
    BASE_URL,
    params=params,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30
)

# Para debug: print a URL final e um pedaço do HTML
print("URL requisitada:", response.url)
print("HTML inicial:", response.text[:500])  # Adicione isso no GitHub Actions para ver o output

soup = BeautifulSoup(response.text, "html.parser")

no_result = soup.find(
    "td",
    string=lambda t: t and "No character auctions found." in t
)

has_auction = soup.find(
    "a",
    href=lambda h: h and "auctionid" in h  # Ajustado para o formato real dos links de detalhes
)

if no_result:
    resultado = f"❌ {PERSONAGEM}: não encontrado"
elif has_auction:
    resultado = f"✅ {PERSONAGEM}: encontrado"
else:
    resultado = f"⚠️ {PERSONAGEM}: resultado inconclusivo"

print(resultado)
enviar_telegram(resultado)