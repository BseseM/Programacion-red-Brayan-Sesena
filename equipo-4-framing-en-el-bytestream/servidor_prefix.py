import socket
import struct

# Configuraci0n del servidor 
HOST = "127.0.0.1"
PORT = 5050
HEADER_SIZE_BYTES = 4
BYTE_ORDER_FORMAT = ">I"  # Big-Endian (Network Byte Order) + Unsigned Int (4 bytes)


def receive_exact_bytes(connection: socket.socket, target_length: int) -> bytes:
    """
    Un unico recv() no garantiza
    recibir todos los bytes solicitados. Esta funcion acumula trozos en un buffer
    hasta completar la cantidad exacta
    """
    received_buffer = bytearray()
    while len(received_buffer) < target_length:
        remaining_bytes = target_length - len(received_buffer)
        chunk = connection.recv(remaining_bytes)

        # recv() retorna b"" si el otro extremo cerro la conexión TCP ordenadamente
        if not chunk:
            raise ConnectionError("La conexion se cerro antes de recibir todos los datos esperados.")

        received_buffer.extend(chunk)

    return bytes(received_buffer)


def receive_framed_message(connection: socket.socket) -> bytes:
    """
    Aplica el protocolo de dos pasos: primero lee la cabecera fija para descubrir
    cuanto mide el cuerpo, y luego lee la carga util completa.
    """
    raw_header = receive_exact_bytes(connection, HEADER_SIZE_BYTES)
    message_length = struct.unpack(BYTE_ORDER_FORMAT, raw_header)[0]

    return receive_exact_bytes(connection, message_length)


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Permite reutilizar el puerto inmediatamente después de reiniciar el servidor,
    # evitando el estado de espera TIME_WAIT del SO
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Servidor escuchando en {HOST}:{PORT} (Protocolo: Length-Prefix)...")

    # accept() es una llamada bloqueante: el proceso se pausa hasta que un cliente inicie el handshake TCP
    client_connection, client_address = server_socket.accept()

    with client_connection:
        print(f"Cliente conectado desde {client_address}")
        try:
            while True:
                payload = receive_framed_message(client_connection)
                message_text = payload.decode("utf-8")
                print(f"Mensaje recibido [{len(payload)} bytes]: {message_text}")
        except ConnectionError:
            print(f"El cliente {client_address} ha finalizado la sesión.")
        finally:
            server_socket.close()


if __name__ == "__main__":
    start_server()
