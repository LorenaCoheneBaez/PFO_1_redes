from datetime import datetime
import socket
import sqlite3
import sys

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
  except sqlite3.Error as e:
    print(f"[Error] No se pudo acceder a la base de datos: {e}")
    sys.exit(1)

#Guardar mensaje en la base de datos
def guardar_mensaje(contenido, ip_cliente):
  """Guarda un mensaje recibido en la base de datos SQLite."""
  try:
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    fecha_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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
    print(f"[Error de Base de Datos] No se pudo guardar el mensaje: {e}")

# Diccionario de preguntas y respuestas
respuestas = {
    "¿Cuál es la capital de Francia?": "París",
    "¿Cuántos lados tiene un cuadrado?": "4",
    "¿Qué lenguaje usamos?": "Python",
}

# Iniciar socket

def iniciar_server():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Servidor escuchando en {HOST}:{PORT}")
            return s
    except Exception as e:
        print(f"[Error] No se pudo iniciar el servidor: {e}")
        sys.exit(1)

#Aceptar conexiones y recibir mensajes
def aceptar_connectiones(s):
    print("Esperando conexiones...")
    inicializar_db()

    while True:
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

                # Guardar en SQLite
                guardar_mensaje(mensaje, ip_cliente)

                # Responder al cliente
                respuesta = f"Mensaje recibido: {mensaje}"
                conexion_cliente.sendall(respuesta.encode("utf-8"))

        except ConnectionResetError:
            print(f"[Aviso] El cliente {ip_cliente} cerró la conexión abruptamente.")
        except Exception as e:
            print(f"[Error] Ocurrió un error con la conexión: {e}")
        finally:
            conexion_cliente.close()

if __name__ == "__main__":
  # Iniciar servidor
  socket_servidor = iniciar_server()
  try:
    aceptar_connectiones(socket_servidor)
  except KeyboardInterrupt:
    print("\n[Servidor] Servidor detenido manualmente.")
    socket_servidor.close()