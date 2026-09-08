"""Cliente bloqueante para la práctica de Batalla Naval con sockets.

Uso:
    python3 cliente.py 192.168.1.20
    python3 cliente.py 192.168.1.20 5050

El servidor debe estar ejecutándose antes de iniciar este programa.
Cada petición y respuesta termina con un salto de línea para delimitar los
mensajes TCP (TCP es un flujo de bytes, no conserva los límites de mensajes).
"""

from __future__ import annotations

import re
import socket
import sys

PUERTO_PREDETERMINADO = 5050
TAMANO_BUFFER = 1024
PATRON_COORDENADA = re.compile(r"^[A-Ja-j](?:10|[1-9])$")

def recibir_linea(conexion: socket.socket) -> str:
    """Recibe exactamente una respuesta de texto terminada en salto de línea."""
    datos = bytearray()
    while True:
        bloque = conexion.recv(TAMANO_BUFFER)  # bloqueante: espera al servidor
        if not bloque:
            raise ConnectionError("El servidor cerró la conexión.")
        datos.extend(bloque)
        if b"\n" in bloque:
            return bytes(datos).split(b"\n", 1)[0].decode("utf-8").strip()

#Funcion que procesa la coordenada tras establecer conexion
def jugar(ip_servidor: str, puerto: int) -> None:
    """Conecta al defensor y envía ataques hasta que el usuario salga."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((ip_servidor, puerto))  # el cliente inicia la conexión
        print(f"Conectado al defensor en {ip_servidor}:{puerto}.")
        print("Escribe una coordenada, por ejemplo B7 (o 'salir').")

        while True:
            ataque = input("Ataque> ").strip().upper()
            if ataque in {"SALIR", "EXIT", "QUIT"}:
                # Es opcional para el servidor, pero deja explícita la salida.
                cliente.sendall(b"SALIR\n")
                return
            if not PATRON_COORDENADA.fullmatch(ataque):
                print("Coordenada inválida. Usa A1 a J10.")
                continue

            # Regla de oro: texto -> bytes antes de enviar.
            cliente.sendall((ataque + "\n").encode("utf-8"))
            # Regla de oro: bytes -> texto al recibir. Espera bloqueando el turno.
            respuesta = recibir_linea(cliente)
            print(f"Defensor: {respuesta}")

            if respuesta.upper() in {"FIN", "JUEGO TERMINADO", "DERROTA", "VICTORIA"}:
                return

#Uso de la libreia Sys para la entrada de argumentos (IP) desde la linea de comandos
def main() -> None:
    if len(sys.argv) not in {2, 3}:
        print(f"Uso: python3 {sys.argv[0]} IP_DEL_SERVIDOR [PUERTO]")
        raise SystemExit(2)

    ip_servidor = sys.argv[1]
    try:
        puerto = int(sys.argv[2]) if len(sys.argv) == 3 else PUERTO_PREDETERMINADO
        if not 1 <= puerto <= 65535:
            raise ValueError
    except ValueError:
        print("El puerto debe ser un entero entre 1 y 65535.")
        raise SystemExit(2)

    try:
        jugar(ip_servidor, puerto)
    except (ConnectionError, OSError) as error:
        print(f"No fue posible jugar: {error}")
        raise SystemExit(1)
    except KeyboardInterrupt:
        print("\nCliente cerrado.")


if __name__ == "__main__":
    main()
