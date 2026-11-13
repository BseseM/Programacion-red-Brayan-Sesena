import http.server, ssl

servidor = http.server.HTTPServer(("localhost", 8443), http.server.SimpleHTTPRequestHandler)

contexto = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
contexto.load_cert_chain("certificado.pem", "llave.pem")
servidor.socket = contexto.wrap_socket(servidor.socket, server_side=True)
print("Servidor HTTPS en https://localhost:8443")
servidor.serve_forever()

