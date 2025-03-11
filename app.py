import requests
from time import sleep
import yfinance as yf
import win32com.client as win32

# Preços para alerta
ACOES_LISTA = {
    "AAPL": 300,
    "META": 800,
    "AMZN": 300,
    "GOOGL": 200,
    "NVDA": 200,
    "INTR": 50,
    "NU": 50,
}
CRIPTO_LISTA = {
    "BTC": 104000,
    "ETH": 3000,
    "SOL": 300,
    "BNB": 800,
}


# Função para buscar preços das criptomoedas na Binance
def get_crypto_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
    response = requests.get(url)
    data = response.json()
    return float(data["price"])


# Função para buscar preços das ações no Yahoo Finance
def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period="1d")["Close"].iloc[-1]  # Último lançamento de preço


# Função para enviar email
def send_email(msg):
    outlook = win32.Dispatch("outlook.application")

    try:
        mail = outlook.CreateItem(0)
        mail.To = "joaovictorlimametzdorf@gmail.com"
        mail.Subject = "📊 Alerta de Preço - Criptos & Ações"
        mail.Body = msg
        mail.Send()
    except Exception as e:
        print(f"Erro ao enviar email: {e}")


# Monitoramento dos preços
while True:
    msg = ""

    try:
        # Verifica se o preço atual da criptomoeda ultrapassou o alerta
        for cripto, alerta in CRIPTO_LISTA.items():
            preco_atual = get_crypto_price(cripto)
            if preco_atual >= alerta:
                msg += f"🚨 Alerta: O preço da criptomoeda {cripto} ultrapassou U${alerta}! Preço atual: U${preco_atual:.2f}\n"

        # Verifica se o preço atual da ação ultrapassou o alerta
        for acao, alerta in ACOES_LISTA.items():
            preco_atual = get_stock_price(acao)
            if preco_atual >= alerta:
                msg += f"🚨 Alerta: O preço da ação {acao} ultrapassou U${alerta}! Preço atual: U${preco_atual:.2f}\n"

        if msg:
            send_email(msg)
            print("Email enviado!")
        else:
            print("Nenhum alerta para ser enviado.")

        print("Aguardando 30min para o próximo alerta...")
        sleep(1800)  # 30 Minutos
    except Exception as e:
        print(f"Erro ao monitorar preços: {e}")
        print("Aguardando 1min para tentar novamente...")
        sleep(60)  # 1 Minuto
