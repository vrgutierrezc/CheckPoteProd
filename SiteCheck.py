#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import sys

# 1. Fetch and parse the page
URL = "https://www.minenergia.gov.co/es/misional/hidrocarburos/funcionamiento-del-sector/gas-natural/"

try:
    resp = requests.get(URL, timeout=20)
    resp.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"ERROR: No se pudo conectar o descargar la página: {e}", file=sys.stderr)
    sys.exit(3)  # Custom exit code for connection problems

soup = BeautifulSoup(resp.text, "html.parser")

# 2. Find the <p data-block-key="ylaun">
p = soup.select_one('div#collapse0 p[data-block-key="ylaun"]')
if not p:
    print("ERROR: No se encontró el párrafo ylaun")
    sys.exit(2)

# 3. Find the next <ul> sibling
ul = p.find_next_sibling("ul")
if not ul:
    print("ERROR: No se encontró la lista ul después del párrafo ylaun")
    sys.exit(2)

# 4. Count only direct <li> children (first level)
li_count = len([li for li in ul.find_all("li", recursive=False)])

print(f"La lista <ul> después de ylaun tiene {li_count} elemento(s) <li> de primer nivel.")

# 5. Error if there is more than one li
if li_count > 1:
    print("⚠️ ¡Hay más de un elemento <li> en el primer nivel del <ul> después de ylaun!")
    sys.exit(1)
else:
    print("✅ Sólo hay un elemento <li> en el primer nivel del <ul> después de ylaun.")
    sys.exit(0)


