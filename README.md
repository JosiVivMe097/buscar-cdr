# Buscar CDR · Buscador de texto en archivos CorelDRAW (.CDR)

Este proyecto busca **texto dentro de archivos .CDR (CorelDRAW X4+)** leyendo sus XML internos **sin abrir CorelDRAW**.  
Útil cuando hay muchos archivos con nombres genéricos (ej. "credenciales") y necesitas encontrar uno por su **contenido**.

## ¿Cómo funciona?
- Los `.CDR` modernos son contenedores **ZIP** con XML.
- El script abre el `.CDR` como ZIP, lee los **XML internos** y busca el texto.
- Opcionalmente muestra **fragmentos** (snippets) y el nombre del archivo interno donde se encontró.

## Uso (Python)
```bash
python python pytrhbuscar.py
👉 Ingresa la ruta de la carpeta donde buscar: C:\Diseños\Corel\Clientes
🔍 Ingresa el texto a buscar: credencial 2024
