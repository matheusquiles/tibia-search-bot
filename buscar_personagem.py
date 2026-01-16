import os
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def enviar_telegram(mensagem):
    if not TELEGRAM_TOKEN:
        print("ERRO: TELEGRAM_TOKEN não encontrado nas variáveis de ambiente!")
        return
    if not CHAT_ID:
        print("ERRO: TELEGRAM_CHAT_ID não encontrado nas variáveis de ambiente!")
        return
    
    print("Tentando enviar mensagem para o Telegram...")
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            data={
                "chat_id": CHAT_ID,
                "text": mensagem,
                "parse_mode": "Markdown"
            },
            timeout=15
        )
        
        print(f"Status da API Telegram: {r.status_code}")
        if r.status_code == 200:
            print("✅ Mensagem enviada com sucesso!")
        else:
            print(f"❌ Erro na API: {r.status_code} - {r.text[:200]}") 
    except Exception as e:
        print(f"❌ Exceção ao tentar enviar: {str(e)}")


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
    print("Erro HTTP Tibia:", response.status_code)
    exit()

print("Status OK (Tibia)")
print("URL requisitada:", response.url)

soup = BeautifulSoup(response.text, "html.parser")

no_result = soup.find("td", string=lambda t: t and "No character auctions found." in t.strip())
has_auction = soup.find("a", href=lambda h: h and "auctionid" in h)

if no_result:
    resultado = f"❌ {PERSONAGEM}: **não encontrado** no Char Bazaar"
elif has_auction:
    resultado = f"✅ {PERSONAGEM}: **encontrado** no Char Bazaar"
else:
    resultado = f"⚠️ {PERSONAGEM}: resultado **inconclusivo** (verificar manualmente)"

print(resultado)
enviar_telegram(resultado)