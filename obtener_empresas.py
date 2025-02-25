import pandas as pd
import yfinance as yf
import os
import subprocess

# Diccionario con los índices y sus símbolos en Yahoo Finance
indices = {
    "S&P_500": "^GSPC",
    "NASDAQ_100": "^NDX",
    "Dow_Jones": "^DJI",
    "DAX": "^GDAXI",
    "IBEX_35": "^IBEX",
    "CAC_40": "^FCHI",
    "FTSE_100": "^FTSE",
    "Nikkei_225": "^N225",
    "Hang_Seng": "^HSI",
    "Shanghai_Composite": "000001.SS"
}

def obtener_tickers_yfinance(indice):
    """Obtiene los componentes de un índice desde Yahoo Finance."""
    try:
        tickers = yf.Ticker(indice).history(period="1d").columns.tolist()
        return tickers if tickers else []
    except Exception as e:
        print(f"⚠️ Error obteniendo datos de Yahoo Finance para {indice}: {e}")
        return []

# Obtener y guardar los componentes de cada índice
def actualizar_indices():
    for nombre_indice, simbolo in indices.items():
        print(f"🔍 Obteniendo empresas del {nombre_indice}...")
        tickers = obtener_tickers_yfinance(simbolo)
        
        if not tickers:
            print(f"⚠️ No se encontraron datos para {nombre_indice}")
            continue

        df = pd.DataFrame(tickers, columns=["Ticker"])
        df.to_csv(f"{nombre_indice}.csv", index=False)
        print(f"✅ Datos de {nombre_indice} guardados en {nombre_indice}.csv")

def subir_a_github():
    """Sube los archivos actualizados a GitHub automáticamente."""
    print("📤 Subiendo datos actualizados a GitHub...")
    try:
        subprocess.run(["git", "add", "*.csv"], check=True)
        subprocess.run(["git", "commit", "-m", "Actualización automática de listas de empresas"], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
        print("✅ Datos actualizados y subidos a GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Error subiendo datos a GitHub: {e}")

if __name__ == "__main__":
    actualizar_indices()
    subir_a_github()