import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from datetime import datetime

# Configuración
URL = "https://proxy.zeronet.dev/1H3KoazXt2gCJgeD8673eFvQYXG7cbRddU/lista-ace.m3u"
ARCHIVO_SALIDA = "get.txt"
REEMPLAZOS = [" --> NEW ERA", " --> ELCANO", " --> NEW LOOP"]
CANALES_EXCLUIDOS = ["AUTOMOTORSPORT", "CANAL MOTOR", "MOTORS TV", "MOTORVISION", "NBA", "SKY SPORTS ARENA", "SKY SPORTS CRICKET", "SUPERTENNIS", "TENNIS CHANNEL", "TR:", "UFC FIGHT PASS"]

# Parámetros de reintento
INTENTOS_MAXIMOS = 3
ESPERA_ENTRE_INTENTOS = 5

# Descarga la lista con política de reintentos
@retry(stop=stop_after_attempt(INTENTOS_MAXIMOS), wait=wait_fixed(ESPERA_ENTRE_INTENTOS))
def descargar_archivo(url):
    print(f"Descargando archivo desde {url}")
    response = requests.get(url, timeout=10)  # Timeout para evitar esperas indefinidas
    response.raise_for_status()  # Lanza error si la descarga falla
    return response.text

# Elimina los textos especificados en la lista de reemplazos
def modificar_contenido(contenido, reemplazos):
    for reemplazo in reemplazos:
        contenido = contenido.replace(reemplazo, "")
    return contenido

# Añade un canal en la primera línea con la hora de generación del archivo
def agregar_hora_como_canal(contenido):
    fecha_actual = datetime.now().strftime("%d/%m/%Y")  # Formato DD/MM/YYYY
    hora_actual = datetime.now().strftime("%H:%M:%S")   # Formato HH:MM:SS
    canal_hora = f'#EXTINF:-1 tvg-logo="https://www.dl.dropboxusercontent.com/s/11sa5eu1urweo3e/Actualizado.png", {fecha_actual} {hora_actual}\nhttp://127.0.0.1:6878/ace/getstream?id=\n\n'
    contenido = canal_hora + contenido
    return contenido

# Elimina de la lista los canales especificados en la lista de exclusión
def excluir_canales(contenido, canales_excluidos):
    lineas = contenido.splitlines()
    contenido_filtrado = []
    excluir = False

    canales_excluidos_upper = [canal.upper() for canal in canales_excluidos]

    for linea in lineas:
        if linea.startswith("#EXTINF"):
            excluir = any(nombre.upper() in linea.upper() for nombre in canales_excluidos_upper)
        if not excluir:
            contenido_filtrado.append(linea)

    return "\n".join(contenido_filtrado) + "\n"

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
        contenido_sin_excluidos = excluir_canales(contenido_modificado, CANALES_EXCLUIDOS)
        contenido_final = agregar_hora_como_canal(contenido_sin_excluidos)
        guardar_archivo(ARCHIVO_SALIDA, contenido_final)

if __name__ == "__main__":
    main()