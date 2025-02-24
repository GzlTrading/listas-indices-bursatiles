import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from io import StringIO

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

def obtener_tickers_wikipedia(url):
    """Obtiene los tickers de empresas desde Wikipedia detectando automáticamente la tabla correcta."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all("table", {"class": "wikitable"})

        for i, table in enumerate(tables):
            df = pd.read_html(StringIO(str(table)))[0]  # Convertimos la tabla en DataFrame

            for col in df.columns:
                if any(keyword in col.lower() for keyword in ["ticker", "symbol", "code"]):
                    tickers = df[col].dropna().astype(str).tolist()
                    print(f"✅ Encontrada columna '{col}' en {url} (Tabla {i})")
                    return tickers
        print(f"⚠️ No se encontraron tickers en {url}")
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

print("🚀 Proceso completado: Se han guardado todas las listas de empresas de cada índice.")