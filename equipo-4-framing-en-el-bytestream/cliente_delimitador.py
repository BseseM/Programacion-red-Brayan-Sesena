import socket

HOST = "127.0.0.1"
PORT = 5051
DELIMITER_STRING = "\n"


def send_line(connection: socket.socket, message_text: str) -> None:
    """
    Valida que la carga útil no contenga el delimitador para evitar la corrupción
    del framing en el receptor, y adjunta la marca final.
    """
    if DELIMITER_STRING in message_text:
        raise ValueError("El mensaje no puede contener caracteres de salto de línea internamente.")

    formatted_payload = message_text + DELIMITER_STRING
    connection.sendall(formatted_payload.encode("utf-8"))


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    messages_to_send = [
        "Primera línea de texto",
        "Segunda línea enviada mediante delimitador",
        "Tercera línea final",
    ]

    with client_socket:
        for text in messages_to_send:
            send_line(client_socket, text)
            print(f"Línea enviada: '{text}'")


if __name__ == "__main__":
    start_client()
