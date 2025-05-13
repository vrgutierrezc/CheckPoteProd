# Archivo: check_site.py
import requests
from bs4 import BeautifulSoup
import difflib
from pathlib import Path
import sys

# Configuración
URL = "https://www.minenergia.gov.co/es/misional/hidrocarburos/funcionamiento-del-sector/gas-natural/"
SELECTOR = 'p[data-block-key="ylaun"]'
STATE_FILE = Path("prev_content.html")

def fetch_container_html():
    resp = requests.get(URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    elem = soup.select_one(SELECTOR)
    if not elem:
        print(f"ERROR: elemento {SELECTOR} no encontrado", file=sys.stderr)
        sys.exit(2)
    return elem.find_parent("div").prettify()

def main():
    current = fetch_container_html()
    if STATE_FILE.exists():
        old = STATE_FILE.read_text(encoding="utf-8")
    else:
        old = ""
    if old != current:
        # Mostrar diff
        diff = difflib.unified_diff(
            old.splitlines(),
            current.splitlines(),
            fromfile="prev_content.html",
            tofile="current",
            lineterm=""
        )
        print("⚠️ Contenido cambiado:")
        for line in diff:
            print(line)
        # Guardar nuevo estado
        STATE_FILE.write_text(current, encoding="utf-8")
        sys.exit(1)
    else:
        print("✅ Sin cambios.")
        sys.exit(0)

if __name__ == "__main__":
    main()