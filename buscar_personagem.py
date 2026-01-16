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
BASE_URL = "https://www.tibia.com/charactertrade/"

# Parâmetros mínimos necessários
params = {
    "subtopic": "currentcharactertrades",
    "searchstring": PERSONAGEM,
    "searchtype": "3",           # ESSENCIAL: 3 = busca por nome de personagem
    "currentpage": "1",
    "order_column": "101",       # ordenar por data de término
    "order_direction": "1"       # mais antigo primeiro
}

response = requests.get(
    BASE_URL,
    params=params,
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
    timeout=30
)

# Debug: mostra a URL final gerada
print("URL requisitada:", response.url)

soup = BeautifulSoup(response.text, "html.parser")

# Verifica se apareceu a mensagem de "não encontrado"
no_result = soup.find(
    "td",
    string=lambda t: t and "No character auctions found." in t.strip()
)

# Verifica se existe algum link de leilão (o correto é "auctionid", não "auctiondetails")
has_auction = soup.find(
    "a",
    href=lambda h: h and "auctionid" in h
)

if no_result:
    resultado = f"❌ {PERSONAGEM}: **não encontrado** no Char Bazaar"
elif has_auction:
    resultado = f"✅ {PERSONAGEM}: **encontrado** no Char Bazaar"
else:
    resultado = f"⚠️ {PERSONAGEM}: resultado **inconclusivo** (verificar manualmente)"

print(resultado)
enviar_telegram(resultado)