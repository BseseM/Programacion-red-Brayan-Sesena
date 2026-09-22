import socket
import struct

HOST = "127.0.0.1"
PORT = 5050
BYTE_ORDER_FORMAT = ">I"


def send_framed_message(connection: socket.socket, message_bytes: bytes) -> None:
    """
    Empaqueta la longitud del mensaje en un entero de 4 bytes usando la convención
    Network Byte Order (Big-Endian) para garantizar interoperabilidad entre diferentes arquitecturas.
    """
    message_length = len(message_bytes)
    header = struct.pack(BYTE_ORDER_FORMAT, message_length)

    # sendall() maneja internamente reintentos si el socket no puede enviar todo el bloque en una sola llamada
    connection.sendall(header + message_bytes)


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    messages_to_send = [
        "Hola Servidor",
        "Este es un mensaje mas largo con framing por longitud",
        "¡Prueba completada exitosamente!",
    ]

    with client_socket:
        for text in messages_to_send:
            encoded_message = text.encode("utf-8")
            send_framed_message(client_socket, encoded_message)
            print(f"Mensaje enviado correctamente: '{text}'")


if __name__ == "__main__":
    start_client()
