from datetime import datetime
import socket
import sqlite3
import sys

# Diccionario de preguntas y respuestas
respuestas = {
    "hola": "¡Hola! Mensaje recibido: {timestamp}",
    "ayuda": "Servidor de sockets activo. Mensaje recibido: {timestamp}",
    "estado": "El sistema funciona correctamente. Mensaje recibido: {timestamp}",
    "gracias": "¡De nada! Mensaje recibido: {timestamp}",
}

respuesta_genérica = (
    "Mensaje recibido: {timestamp}"
)

HOST= "localhost"
PORT= 5000
DB_NAME = "mensajes.db"

#inicializar la base de datos
def inicializar_db():
  """Inicializa la base de datos SQLite y crea la tabla si no existe."""
  try:
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        """)
    conexion.commit()
    conexion.close()
  except sqlite3.OperationalError as e:
    # Manejo de errores para base de datos no accesible (ej. bloqueada, sin permisos, etc.)
    print(
        f"[Error Crítico] Base de datos no accesible ({DB_NAME}): {e}",
        file=sys.stderr,
    )
    sys.exit(1)
  except sqlite3.Error as e:
    print(f"[Error de Base de Datos] Ocurrió un error inesperado: {e}")
    sys.exit(1)

# Guardar mensaje en la base de datos
def guardar_mensaje(contenido, ip_cliente, fecha_envio):
  """Guarda un mensaje recibido en la base de datos SQLite."""
  try:
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute(
        """
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        """,
        (contenido, fecha_envio, ip_cliente),
    )

    conexion.commit()
    conexion.close()
  except sqlite3.Error as e:
    #Manejo de errores para problemas al guardar el mensaje (ej. base de datos bloqueada, sin permisos, etc.)
    print(
        f"[Error] DB no accesible al intentar guardar el mensaje: {e}",
        file=sys.stderr,
    )
  except sqlite3.Error as e:
    print(
        f"[Error de Base de Datos] No se pudo guardar el mensaje: {e}",
        file=sys.stderr,
    )

 # Configuración del socket TCP/IP
def iniciar_server():
  """Inicializa y configura el socket del servidor."""
  try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Servidor escuchando en {HOST}:{PORT}")
    return s
  except Exception as e:
   # Manejo específico para puerto ocupado o errores de enlace (Bind)
    if e.winerror == 10048 or "Address already in use" in str(e):
      print(
          f"[Error Crítico] El puerto {PORT} ya se encuentra ocupado por otra"
          f" aplicación.",
          file=sys.stderr,
      )
    else:
      print(
          f"[Error Crítico] Error de red al iniciar el servidor en el puerto"
          f" {PORT}: {e}",
          file=sys.stderr,
      )
    sys.exit(1)
  except Exception as e:
    print(
        f"[Error Crítico] No se pudo iniciar el servidor: {e}", file=sys.stderr
    )
    sys.exit(1)

# Aceptar conexiones y procesar mensajes
def aceptar_conecciones(s):
  """Acepta conexiones y procesa los mensajes usando el diccionario."""
  print("Esperando conexiones...")
  inicializar_db()

  while True:
    conexion_cliente = None
    ip_cliente = "Desconocida"
    try:
      conexion_cliente, direccion = s.accept()
      ip_cliente = direccion[0]
      print(f"[Conexión] Conectado desde {ip_cliente}:{direccion[1]}")

      while True:
        datos = conexion_cliente.recv(1024)
        if not datos:
          break

        mensaje = datos.decode("utf-8").strip()
        print(f"[Mensaje recibido de {ip_cliente}]: {mensaje}")

        # Comprobar si el cliente envió éxito para finalizar la conexión
        if mensaje.lower() == "éxito":
          print(f"[Aviso] El cliente {ip_cliente} solicitó finalizar la conexión.")
          respuesta = "Conexión finalizada con éxito."
          conexion_cliente.sendall(respuesta.encode("utf-8"))
          break

        # Generar el timestamp actual para el mensaje
        timestamp_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Guardar el mensaje original en SQLite
        guardar_mensaje(mensaje, ip_cliente, timestamp_actual)

        # Buscar respuesta en el diccionario
        mensaje_lower = mensaje.lower()
        plantilla_respuesta = respuestas.get(
            mensaje_lower, respuesta_genérica
        )
        respuesta = plantilla_respuesta.format(timestamp=timestamp_actual)

        # Enviar la respuesta genérica
        conexion_cliente.sendall(respuesta.encode("utf-8"))

    except ConnectionResetError:
      print(f"[Aviso] El cliente {ip_cliente} cerró la conexión abruptamente.")
    except Exception as e:
      print(f"[Error] Ocurrió un error con la conexión: {e}")
    finally:
      if conexion_cliente is not None:
        try:
          conexion_cliente.close()
          print(f"[Conexión] Socket cerrado para {ip_cliente}\n")
        except Exception:
          pass


if __name__ == "__main__":
  socket_servidor = iniciar_server()
  try:
    aceptar_conecciones(socket_servidor)
  except KeyboardInterrupt:
    print("\n[Servidor] Servidor detenido manualmente.")
    socket_servidor.close()