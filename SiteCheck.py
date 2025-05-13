#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import difflib
import sys
import re

# Configuración
URL         = "https://www.minenergia.gov.co/es/misional/hidrocarburos/funcionamiento-del-sector/gas-natural/"
DIV_SELECTOR = "div#collapse0"
P_SELECTOR   = 'p[data-block-key="ylaun"]'

EXPECTED_TEXT = (
    "El Ministerio de Minas y Energía informa qué, el cronograma para el reporte de la "
    "declaración de producción de gas natural para el periodo 2024-2033, podrá encontrarlo "
    "en los siguientes enlaces."
)

def normalize(txt: str) -> str:
    # Collapse all whitespace to single spaces
    return re.sub(r"\s+", " ", txt.strip())

def main():
    # 1) Fetch and parse
    resp = requests.get(URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    # 2) Locate the container and paragraph
    div = soup.select_one(DIV_SELECTOR)
    if not div:
        print(f"ERROR: No se encontró el {DIV_SELECTOR}", file=sys.stderr)
        sys.exit(2)

    p = div.select_one(P_SELECTOR)
    if not p:
        print(f"ERROR: No se encontró el {P_SELECTOR}", file=sys.stderr)
        sys.exit(2)

    # 3) Normalize both expected and current
    current = normalize(p.get_text(separator=" ", strip=True))
    expected = normalize(EXPECTED_TEXT)

    # 4) Compare
    if current != expected:
        print("⚠️ ¡El contenido ha cambiado! Aquí está el diff:\n")
        diff = difflib.unified_diff(
            expected.split(),
            current.split(),
            fromfile="expected",
            tofile="current",
            lineterm=""
        )
        for line in diff:
            print(line)
        sys.exit(1)

    print("✅ El párrafo coincide exactamente.")
    sys.exit(0)

if __name__ == "__main__":
    main()
