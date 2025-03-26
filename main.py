import requests
from tenacity import retry, stop_after_attempt, wait_fixed

# Configuración
URL = "https://proxy.zeronet.dev/1H3KoazXt2gCJgeD8673eFvQYXG7cbRddU/lista-ace.m3u"
ARCHIVO_SALIDA = "get.txt"
REEMPLAZOS = [" --> NEW ERA", " --> ELCANO", " --> NEW LOOP"]

# Parámetros de reintento
INTENTOS_MAXIMOS = 3
ESPERA_ENTRE_INTENTOS = 5

# Descarga la lista con política de reintentos
@retry(stop=stop_after_attempt(INTENTOS_MAXIMOS), wait=wait_fixed(ESPERA_ENTRE_INTENTOS))
def descargar_archivo(url):
    print(f"Descargando archivo desde {url}...")
    response = requests.get(url, timeout=10)  # Timeout para evitar esperas indefinidas
    response.raise_for_status()  # Lanza error si la descarga falla
    return response.text

# Elimina los textos especificados en la lista de reemplazos
def modificar_contenido(contenido, reemplazos):
    for reemplazo in reemplazos:
        contenido = contenido.replace(reemplazo, "")
    return contenido

# Guarda el contenido en un archivo
def guardar_archivo(nombre_archivo, contenido):
    
    try:
        with open(nombre_archivo, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
        print(f"Archivo guardado como '{nombre_archivo}' con reemplazos realizados correctamente.")
    except IOError as e:
        print(f"Error al guardar el archivo: {e}")

# Función principal que coordina la ejecución del script
def main():
    contenido = descargar_archivo(URL)
    if contenido:
        contenido_modificado = modificar_contenido(contenido, REEMPLAZOS)
        guardar_archivo(ARCHIVO_SALIDA, contenido_modificado)

if __name__ == "__main__":
    main()