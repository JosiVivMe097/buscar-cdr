import os
import zipfile
from pathlib import Path
import re
import html

# Extensiones internas típicas con texto
TEXTLIKE_EXTS = {".xml", ".rels", ".txt"}

# Intentos de decodificación para XML
DECODINGS = ["utf-8", "utf-16", "cp1252", "latin-1"]

def iter_cdr_files(root: Path):
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if fn.lower().endswith(".cdr"):
                yield Path(dirpath) / fn

def read_member_safely(zf: zipfile.ZipFile, name: str) -> str | None:
    try:
        data = zf.read(name)
    except Exception:
        return None

    ext = Path(name).suffix.lower()
    if ext not in TEXTLIKE_EXTS and "xml" not in name.lower():
        return None

    for enc in DECODINGS:
        try:
            return data.decode(enc, errors="strict")
        except Exception:
            continue
    return data.decode("utf-8", errors="ignore")

def search_in_cdr_zip(cdr_path: Path, pattern: re.Pattern, context: int = 80):
    try:
        if not zipfile.is_zipfile(cdr_path):
            return False, []

        with zipfile.ZipFile(cdr_path) as zf:
            for name in zf.namelist():
                txt = read_member_safely(zf, name)
                if not txt:
                    continue
                txt_plain = html.unescape(txt)

                m = pattern.search(txt_plain)
                if m:
                    snippets = []
                    for match in pattern.finditer(txt_plain):
                        start = max(0, match.start() - context)
                        end = min(len(txt_plain), match.end() + context)
                        snippet = txt_plain[start:end].replace("\r", " ").replace("\n", " ")
                        snippets.append((name, snippet))
                        if len(snippets) >= 3:
                            break
                    return True, snippets
        return False, []
    except Exception:
        return False, []

def main():
    # Pedir datos al usuario
    ruta = input("👉 Ingresa la ruta de la carpeta donde buscar: ").strip('" ')
    if not ruta:
        print("ERROR: No ingresaste ninguna ruta.")
        return
    root = Path(ruta).expanduser()
    if not root.exists() or not root.is_dir():
        print(f"ERROR: La carpeta no existe o no es válida: {root}")
        return

    busqueda = input("🔍 Ingresa el texto a buscar: ").strip()
    if not busqueda:
        print("ERROR: No ingresaste ningún texto de búsqueda.")
        return

    # Patrón de búsqueda (no distingue mayúsculas/minúsculas)
    pattern = re.compile(re.escape(busqueda), re.IGNORECASE)

    total = 0
    hits = 0

    print("\n⏳ Buscando, por favor espera...\n")
    for cdr in iter_cdr_files(root):
        total += 1
        found, snippets = search_in_cdr_zip(cdr, pattern)
        if found:
            hits += 1
            print(f"✔ {cdr}")
            for inner_name, snippet in snippets:
                print(f"   - [{inner_name}] ...{snippet}...")

        elif total % 100 == 0:
            print(f"[Progreso] Archivos revisados: {total}")

    print("\n=== RESUMEN ===")
    print(f"Archivos .CDR revisados: {total}")
    print(f"Archivos con coincidencias: {hits}")

if __name__ == "__main__":
    main()
