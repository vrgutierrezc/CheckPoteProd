import requests
from bs4 import BeautifulSoup
import hashlib
import difflib
from pathlib import Path

# Configuración
URL = "https://www.minenergia.gov.co/es/misional/hidrocarburos/funcionamiento-del-sector/gas-natural/"
SELECTOR = 'p[data-block-key="ylaun"]'

import requests
from bs4 import BeautifulSoup
import hashlib
import difflib
from pathlib import Path

# Configuración
URL = "https://www.minenergia.gov.co/es/misional/hidrocarburos/funcionamiento-del-sector/gas-natural/"
SELECTOR = 'p[data-block-key="ylaun"]'

def fetch_element_html():
    """Descarga la página y devuelve el HTML del contenedor deseado."""
    resp = requests.get(URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    p = soup.select_one(SELECTOR)
    if not p:
        raise ValueError("Elemento con selector {} no encontrado".format(SELECTOR))
    return p.find_parent("div").prettify()

# Rutas locales
prev_file = Path("prev_content.html")
hash_file = Path("prev_hash.txt")

# Obtener contenido y hash actuales
current_html = fetch_element_html()
current_hash = hashlib.sha256(current_html.encode("utf-8")).hexdigest()

# Leer hash previo si existe
prev_hash = hash_file.read_text().strip() if hash_file.exists() else None

# Comparar y mostrar diff si cambió
if prev_hash != current_hash:
    print("Cambio detectado en el contenido.")
    if prev_file.exists():
        old_html = prev_file.read_text(encoding="utf-8")
        diff = difflib.unified_diff(
            old_html.splitlines(),
            current_html.splitlines(),
            fromfile="prev_content.html",
            tofile="current_content.html",
            lineterm=""
        )
        for line in diff:
            print(line)
    # Guardar nueva versión
    prev_file.write_text(current_html, encoding="utf-8")
    hash_file.write_text(current_hash)
else:
    print("No hay cambios desde la última ejecución.")


# Rutas locales
prev_file = Path("prev_content.html")
hash_file = Path("prev_hash.txt")

# Obtener contenido y hash actuales
current_html = fetch_element_html()
current_hash = hashlib.sha256(current_html.encode("utf-8")).hexdigest()

# Leer hash previo si existe
prev_hash = hash_file.read_text().strip() if hash_file.exists() else None

# Comparar y mostrar diff si cambió
if prev_hash != current_hash:
    print("Cambio detectado en el contenido.")
    if prev_file.exists():
        old_html = prev_file.read_text(encoding="utf-8")
        diff = difflib.unified_diff(
            old_html.splitlines(),
            current_html.splitlines(),
            fromfile="prev_content.html",
            tofile="current_content.html",
            lineterm=""
        )
        for line in diff:
            print(line)
    # Guardar nueva versión
    prev_file.write_text(current_html, encoding="utf-8")
    hash_file.write_text(current_hash)
else:
    print("No hay cambios desde la última ejecución.")
