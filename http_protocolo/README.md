# Protocolo HTTP
Esta práctica se dividio en 2 partes

## Parte 1
Se exploro el tŕafico HTTP de sitios web desde el navegador
y con ayuda de la herramienta Insepccionar y en el apartado Network,
se exploraron los encabezados, versiones de HTTP, códigos de respuesta,
user-agent, etc.
+ Se recolecto la información de 6 sitios diferentes.

## Parte 2
Se realizaron métodos, encabezados y códigos de estado a mano con curl y netcat.
Las pruebas se hicieron sobre el servidor httpbin.org, que es un servidor que responde 
lo que se le pida.
+ Algunos de los comandos ejecutados fueron:
```bash
curl -v https://httpbin.org/get   # -v: muestra la petición y la respuesta
curl -i https://httpbin.org/get   # -i: muestra solo los encabezados de respuesta
curl -X POST -d "apodo=ana" \	  # -X: método; -d: cuerpo
-H "Content-Type: text/plain" \
https://httpbin.org/post

printf "GET /get HTTP/1.1\\r\\nHost: httpbin.org\\r\\n\\r\\n" | nc httpbin.org 80
```



