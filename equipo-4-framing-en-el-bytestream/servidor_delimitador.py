import socket

HOST = "127.0.0.1"
PORT = 5051
BUFFER_READ_SIZE = 4096
DELIMITER = b"\n"


class LineStreamReader:
    """
    Mantiene un buffer interno para gestionar la fragmentación de TCP.
    A diferencia de Length Prefix, no sabemos la longitud previa, por lo que
    debemos acumular datos en memoria hasta encontrar el delimitador.
    """

    def __init__(self, connection: socket.socket):
        self.connection = connection
        self.internal_buffer = b""

    def read_line(self) -> str | None:
        while DELIMITER not in self.internal_buffer:
            chunk = self.connection.recv(BUFFER_READ_SIZE)

            # Si recv() retorna b"", la conexion fue cerrada por el cliente
            if not chunk:
                return None

            self.internal_buffer += chunk

        # Se separa exactamente en la primera ocurrencia del delimitador.
        # El sobrante se preserva en internal_buffer para la siguiente llamada.
        raw_line, self.internal_buffer = self.internal_buffer.split(DELIMITER, 1)
        return raw_line.decode("utf-8")


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Servidor escuchando en {HOST}:{PORT} (Protocolo: Delimitador '\\n')...")

    client_connection, client_address = server_socket.accept()

    with client_connection:
        print(f"Cliente conectado desde {client_address}")
        stream_reader = LineStreamReader(client_connection)

        while True:
            received_line = stream_reader.read_line()
            if received_line is None:
                print("El cliente cerró la conexion.")
                break

            print(f"Línea recibida: {received_line}")

    server_socket.close()


if __name__ == "__main__":
    start_server()
