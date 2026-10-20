# Ejercicio La fila basado en socket reimplementado en XML
El ejercicio tuvo como proposito comprender el cambio entre ambas implementaciones, y como los sockets son parte de la base de la comunicacion con XML.
El ejercicio consta de 2 programas.
+ fila_rpc_servidor.py: que es el servidor que registra 2 funciones.
  - tomar_tunor(): Que devuelve el numero de turnos (consecutivo, proyegido con threadinf.Lock)
  - cuantos_van(): Devuelve el numero total de turnos asigados
+ cliente_fila.py
  - El cliente pide el apodo por teclado, llama a las funciones y muestra los resultados

## Ejecución de los programas
- Ejecutar primero el servidor y luego el cliente
  ```bash
  python3 fila_rpc_servidor.py
  python3 cliente_fila.py
  ```
