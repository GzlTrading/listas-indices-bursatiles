import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import os
import subprocess

# Obtener API Key desde la variable de entorno
API_KEY = os.getenv("FMP_API_KEY")

# Diccionario con los índices y sus fuentes
indices = {
    "S&P_500": "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
    "NASDAQ_100": "https://en.wikipedia.org/wiki/NASDAQ-100",
    "Dow_Jones": "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average",
    "DAX": "^GDAXI",
    "IBEX_35": "^IBEX",
    "CAC_40": "^FCHI",
    "FTSE_100": "^FTSE",
    "Nikkei_225": "^N225",
    "Hang_Seng": "^HSI",
    "Shanghai_Composite": "000001.SS"
}

def obtener_tickers_fmp(indice):
    """Obtiene la lista de empresas desde Financial Modeling Prep"""
    if not API_KEY:
        print("⚠️ Error: No se encontró una API Key configurada en la variable de entorno FMP_API_KEY")
        return []
    
    url = f"https://financialmodelingprep.com/api/v3/{indice}_constituent?apikey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        return [empresa["symbol"] for empresa in data]
    except Exception as e:
        print(f"⚠️ Error obteniendo datos de FMP para {indice}: {e}")
        return []

def obtener_tickers_wikipedia(url, table_index=0):
    """Obtiene los tickers de empresas desde Wikipedia."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all("table", {"class": "wikitable"})
        df = pd.read_html(str(tables[table_index]))[0]
        
        for col in df.columns:
            if "Ticker" in col or "Symbol" in col:
                return df[col].dropna().tolist()
    except Exception as e:
        print(f"⚠️ Error obteniendo datos de {url}: {e}")
    return []

# Obtener y guardar los componentes de cada índice
for nombre_indice, fuente in indices.items():
    print(f"🔍 Obteniendo empresas del {nombre_indice}...")
    tickers = []
    
    # Intentar obtener datos de FMP primero
    tickers = obtener_tickers_fmp(nombre_indice.lower())
    
    # Si FMP no devuelve datos, intentar con Wikipedia
    if not tickers and "wikipedia.org" in fuente:
        tickers = obtener_tickers_wikipedia(fuente)
    
    # Si FMP y Wikipedia fallan, intentar con Yahoo Finance
    if not tickers and not "wikipedia.org" in fuente:
        try:
            tickers = list(yf.Ticker(fuente).history(period="1d").columns)
        except Exception as e:
            print(f"⚠️ No se pudieron obtener datos desde Yahoo Finance para {nombre_indice}: {e}")
    
    if not tickers:
        print(f"⚠️ No se encontraron datos para {nombre_indice}")
        continue

    df = pd.DataFrame(tickers, columns=["Ticker"])
    df.to_csv(f"{nombre_indice}.csv", index=False)
    print(f"✅ Datos de {nombre_indice} guardados en {nombre_indice}.csv")

# Subir archivos a GitHub automáticamente
print("📤 Subiendo datos actualizados a GitHub...")
try:
    subprocess.run(["git", "add", "*.csv"], check=True)
    subprocess.run(["git", "commit", "-m", "Actualización automática de listas de empresas"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("✅ Datos actualizados y subidos a GitHub.")
except subprocess.CalledProcessError as e:
    print(f"⚠️ Error subiendo datos a GitHub: {e}")
