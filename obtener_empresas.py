import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import os

# Diccionario con los índices y sus fuentes
indices = {
    "S&P_500": "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",
    "NASDAQ_100": "https://en.wikipedia.org/wiki/NASDAQ-100",
    "Dow_Jones": "https://en.wikipedia.org/wiki/Dow_Jones_Industrial_Average",
    "DAX": "https://en.wikipedia.org/wiki/DAX",
    "IBEX_35": "https://en.wikipedia.org/wiki/IBEX_35",
    "CAC_40": "https://en.wikipedia.org/wiki/CAC_40",
    "FTSE_100": "https://en.wikipedia.org/wiki/FTSE_100_Index",
    "Nikkei_225": "https://en.wikipedia.org/wiki/Nikkei_225",
    "Hang_Seng": "https://en.wikipedia.org/wiki/Hang_Seng_Index",
    "Shanghai_Composite": "https://en.wikipedia.org/wiki/Shanghai_Composite_Index"
}

def obtener_tickers_wikipedia(url, table_index=0):
    """Obtiene los tickers de empresas desde Wikipedia."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all("table", {"class": "wikitable"})
        
        if not tables:
            print(f"⚠️ No se encontraron tablas en {url}")
            return []

        df = pd.read_html(str(tables[table_index]))[0]
        
        for col in df.columns:
            if "Ticker" in col or "Symbol" in col or "Code" in col:
                print(f"✅ Encontrada columna '{col}' en {url} (Tabla {table_index})")
                return df[col].dropna().tolist()
    except Exception as e:
        print(f"⚠️ Error obteniendo datos de {url}: {e}")
    return []

# Obtener y guardar los componentes de cada índice
for nombre_indice, fuente in indices.items():
    print(f"🔍 Obteniendo empresas del {nombre_indice}...")
    try:
        tickers = obtener_tickers_wikipedia(fuente)
        
        if not tickers:
            print(f"⚠️ No se encontraron datos para {nombre_indice}")
            continue

        df = pd.DataFrame(tickers, columns=["Ticker"])
        df.to_csv(f"{nombre_indice}.csv", index=False)
        print(f"✅ Datos de {nombre_indice} guardados en {nombre_indice}.csv")
    except Exception as e:
        print(f"❌ Error obteniendo datos para {nombre_indice}: {e}")

# Subir automáticamente a GitHub
print("📤 Subiendo datos actualizados a GitHub...")
os.system("git add .")
os.system('git commit -m "Actualización automática de listas de empresas"')
os.system("git push origin main")
print("✅ Datos actualizados y subidos a GitHub.")
