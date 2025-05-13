import requests
from bs4 import BeautifulSoup
import difflib
import re

# 1) Fetch the page
URL = "https://www.minenergia.gov.co/es/misional/hidrocarburos/funcionamiento-del-sector/gas-natural/"
resp = requests.get(URL)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")

# 2) Extract and normalize the <p data-block-key="ylaun">
p = soup.select_one('p[data-block-key="ylaun"]')
if not p:
    raise RuntimeError("Element not found")
fetched = p.get_text(separator=" ", strip=True)
# collapse all whitespace to single spaces
fetched = re.sub(r"\s+", " ", fetched)

# 3) Your expected text (also normalized)
expected = (
    "El Ministerio de Minas y Energía informa qué, "
    "el cronograma para el reporte de la declaración de producción de gas natural "
    "para el periodo 2024-2033, podrá encontrarlo en los siguientes enlaces."
)
expected = re.sub(r"\s+", " ", expected.strip())

# 4) Compare and print a diff if they differ
if fetched != expected:
    print("❗ Text mismatch detected:")
    diff = difflib.unified_diff(
        expected.split(),
        fetched.split(),
        fromfile="expected",
        tofile="fetched",
        lineterm=""
    )
    print(" ", " ".join(expected.split()), sep="\n")
    print(" vs ")
    print(" ", " ".join(fetched.split()), sep="\n")
    print("\nDetailed diff:")
    for line in diff:
        print(line)
else:
    print("✅ Text matches exactly!")
