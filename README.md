# Proyecto de redes: servidor y cliente TCP

Este proyecto implementa una comunicación simple entre un cliente y un servidor usando sockets TCP en Python. El servidor recibe mensajes del cliente, responde con mensajes predefinidos y guarda cada mensaje en una base de datos SQLite.

## Archivos

- `servidor.py`: código del servidor.
- `cliente.py`: código del cliente.
- `mensajes.db`: base de datos SQLite creada automáticamente al iniciar el servidor.

## Funcionalidad

- El servidor escucha conexiones en `localhost:5000`.
- El cliente puede enviar mensajes al servidor.
- El servidor responde según el contenido del mensaje:
  - `hola`
  - `ayuda`
  - `estado`
  - `gracias`
- Si el mensaje no coincide con ninguna respuesta conocida, devuelve un mensaje genérico.
- Cada mensaje recibido se guarda en la base de datos con:
  - contenido del mensaje
  - fecha y hora
  - IP del cliente
- Para finalizar la conexión, el cliente puede enviar `éxito`.

## Requisitos

- Python 3.x
- Sistema operativo con soporte para sockets TCP

## Cómo ejecutar

### 1) Iniciar el servidor

```bash
python servidor.py
```

Se mostrará un mensaje indicando que el servidor está escuchando en `localhost:5000`.

### 2) Iniciar el cliente

En otra terminal, ejecutar:

```bash
python cliente.py
```

Luego ingresar mensajes desde el cliente. Por ejemplo:

```text
Mensaje a enviar: hola
Mensaje a enviar: estado
Mensaje a enviar: éxito
```

## Observaciones

- Si el puerto `5000` ya está en uso, el servidor mostrará un error y no podrá iniciarse.
- La base de datos se crea automáticamente la primera vez que se ejecuta el servidor.
- El cliente se desconecta al escribir `éxito`.

## Ejemplo de flujo

1. Se ejecuta el servidor.
2. Se ejecuta el cliente.
3. El cliente envía un mensaje.
4. El servidor responde.
5. El servidor guarda el mensaje en SQLite.
6. Cuando el cliente escribe `éxito`, la conexión termina.
