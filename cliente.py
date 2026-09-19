import socket

HOST= "localhost"
PORT= 5000

# Configuración del socket TCP/IP
def ejecutar_cliente():
  """Conecta al servidor y permite enviar múltiples mensajes hasta escribir 'éxito'."""
  try:
    # Configuración del socket
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect((HOST, PORT))
    print(f"[Cliente] Conectado al servidor {HOST}:{PORT}")
    print("Escribí tus mensajes. Escribí 'éxito' para terminar.\n")

    while True:
      mensaje = input("Mensaje a enviar: ")

      if not mensaje.strip():
        continue

      # Enviar mensaje al servidor
      cliente_socket.sendall(mensaje.encode("utf-8"))

      if mensaje.lower() == "éxito":
        print("[Cliente] Finalizando conexión...")
        break

      # Recibir respuesta del servidor
      respuesta = cliente_socket.recv(1024).decode("utf-8")
      print(f"[Respuesta del servidor] -> {respuesta}\n")

  except ConnectionRefusedError:
    print(
        "[Error] No se pudo conectar al servidor. Asegurate de que esté"
        " encendido."
    )
  except Exception as e:
    print(f"[Error] Ocurrió un error inesperado: {e}")
  finally:
    cliente_socket.close()
    print("[Cliente] Desconectado.")


if __name__ == "__main__":
  ejecutar_cliente()