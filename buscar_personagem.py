import os
import requests
from bs4 import BeautifulSoup

# ... (seu código de telegram e variáveis)

PERSONAGEM = "Telescopio Refrator"
BASE_URL = "https://www.tibia.com/charactertrade/"

params = {
    "subtopic": "currentcharactertrades",
    "searchstring": PERSONAGEM,
    "searchtype": "3",
    "currentpage": "1",
    "order_column": "101",
    "order_direction": "1"
}

response = requests.get(
    BASE_URL,
    params=params,
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
    timeout=30
)

if response.status_code != 200:
    print("Erro HTTP:", response.status_code)
    print(response.text[:500])
    exit()  # ou continue, dependendo do que quiser

print("Status OK")
print("URL requisitada:", response.url)

# Agora sim, cria o soup
soup = BeautifulSoup(response.text, "html.parser")

# Debug depois do soup criado
print("Título da página:", soup.title.string if soup.title else "Sem título")

# Continuação do seu código...
no_result = soup.find(
    "td",
    string=lambda t: t and "No character auctions found." in t.strip()
)

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
# enviar_telegram(resultado)  # descomente quando quiser