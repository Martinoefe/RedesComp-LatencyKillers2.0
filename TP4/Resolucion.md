# Trabajo Práctico N°4 – Redes de Computadoras
 
## Integrantes

* Antonino, Tadeo - [tadeo.antonino@mi.unc.edu.ar](mailto:tadeo.antonino@mi.unc.edu.ar)
* Quintana, Ignacio Agustin - [ignacio.agustin.quintana@mi.unc.edu.ar](mailto:ignacio.agustin.quintana@mi.unc.edu.ar)
* Fioramonti, Martino - [martino.fioramonti@mi.unc.edu.ar](mailto:martino.fioramonti@mi.unc.edu.ar)

---
 
## Punto 1 — Serialización en redes de computadoras
 
### a) ¿Qué es la serialización en redes de computadoras?
 
Cuando dos programas se comunican a través de una red, no pueden simplemente "pasarse" un objeto o estructura de datos directamente, ya que cada programa corre en su propio espacio de memoria, posiblemente en máquinas distintas con arquitecturas distintas. Para que la información pueda viajar por la red, necesita ser convertida a una forma transmisible: una secuencia de bytes.
 
**La serialización es el proceso de convertir una estructura de datos (un objeto, un diccionario, una lista, etc.) en una secuencia de bytes o caracteres que pueda ser transmitida por la red, almacenada, y luego reconstruida por quien la recibe.** El proceso inverso —reconstruir la estructura de datos original a partir de los bytes recibidos— se llama **deserialización**.
 
Por ejemplo, si tenemos el siguiente diccionario en Python (ejemplo que se va a utilizar en el punto 2):
 
```python
datos = {
    "group": "Latency_Killers2.0",
    "payload": "hola server"
}
```
 
Este objeto vive en la memoria RAM de nuestra computadora. Para enviarlo por TCP, lo serializamos a texto JSON:
 
```
{"group": "Latency_Killers2.0", "payload": "hola server"}
```
 
Esa cadena de texto puede viajar como bytes a través de la red. Del otro lado, el servidor la recibe y la deserializa, reconstruyendo el diccionario original para poder trabajar con él.
 
Sin serialización, sería imposible que dos programas escritos en distintos lenguajes, corriendo en distintas máquinas, intercambien datos estructurados de forma confiable y estandarizada.
 
---
 
### b) Diferencia entre serialización binaria y no binaria
 
#### Serialización no binaria (basada en texto)
 
Los datos se representan como texto legible por humanos, utilizando caracteres ASCII o UTF-8. Cualquier persona puede abrir el mensaje y entender su contenido sin herramientas especiales.
 
**Ejemplos:**
- **JSON** (JavaScript Object Notation): el formato más utilizado hoy en día en APIs y servicios web.
- **XML** (eXtensible Markup Language): más verboso, ampliamente usado en sistemas empresariales y servicios SOAP.
- **CSV** (Comma-Separated Values): utilizado para datos tabulares simples.
- **YAML**: muy popular en archivos de configuración.
 
**Ventajas:**
- Legible por humanos sin herramientas especiales, lo que facilita enormemente el debugging.
- Interoperable entre prácticamente cualquier lenguaje de programación.
- Fácil de inspeccionar con herramientas como Wireshark o directamente en una terminal.
- Amplio soporte nativo: Python, por ejemplo, incluye el módulo `json` en su librería estándar.

**Desventajas:**
- Ocupa más espacio: el número `1000000` en JSON ocupa 7 bytes como texto, mientras que en binario puro ocuparía solo 4 bytes.
- Más lento de parsear, especialmente con mensajes de gran tamaño.
- Tipos de datos limitados: JSON, por ejemplo, no distingue entre enteros y floats de forma explícita, ni tiene soporte nativo para fechas o datos binarios.
---
 
#### Serialización binaria
 
Los datos se representan directamente en bytes, sin pasar por una representación de texto legible. El formato está diseñado para ser procesado por máquinas de manera eficiente, no para ser leído por humanos.
 
**Ejemplos:**
- **Protocol Buffers (protobuf)**: desarrollado por Google, muy eficiente y con esquema de datos definido explícitamente.
- **MessagePack**: conceptualmente similar a JSON pero representado en binario, mucho más compacto.
- **Apache Avro**: utilizado en ecosistemas de Big Data como Apache Kafka.
- **BSON** (Binary JSON): usado internamente por MongoDB para almacenar documentos.

**Ventajas:**
- Mucho más compacto: menos bytes transmitidos implica menor uso de ancho de banda y menor latencia.
- Más rápido de serializar y deserializar, especialmente en sistemas de alto volumen.
- Permite representar tipos de datos complejos de forma nativa: fechas, números de precisión arbitraria, datos binarios raw, etc.
- Ideal para sistemas con restricciones de rendimiento o ancho de banda: IoT, videojuegos en red, comunicación entre microservicios, etc.

**Desventajas:**
- No es legible por humanos: para inspeccionar un mensaje se necesitan herramientas específicas.
- Más difícil de depurar, ya que los errores no son visibles a simple vista.
- Algunos formatos (como protobuf) requieren un esquema compartido entre cliente y servidor, lo que agrega complejidad al desarrollo y al mantenimiento.
---
 
#### Tabla comparativa
 
| Característica | No binaria (JSON, XML) | Binaria (protobuf, MessagePack) |
|---|---|---|
| Legibilidad humana | Alta | Nula |
| Tamaño del mensaje | Mayor | Menor |
| Velocidad de parsing | Menor | Mayor |
| Facilidad de debugging | Alta | Baja |
| Interoperabilidad | Muy alta | Alta (requiere esquema en algunos casos) |
| Casos de uso típicos | APIs REST, configuración, logs | Sistemas de alto rendimiento, IoT, microservicios |
 
En el contexto de este trabajo práctico utilizamos **JSON**, un formato de serialización no binaria, por su simplicidad, legibilidad y amplio soporte en Python a través del módulo `json`.

---
 
## Punto 2 — Despliegue del servidor TCP multi-hilo y prueba con PacketSender
 
### ¿Qué es un servidor TCP multi-hilo?
 
El servidor provisto por la cátedra (`server.py`) es un programa Python que escucha conexiones entrantes a través del protocolo TCP. Es **multi-hilo** porque cada vez que un cliente se conecta, el servidor crea un hilo de ejecución nuevo (`threading.Thread`) dedicado exclusivamente a atender a ese cliente. Esto permite que múltiples clientes se conecten y envíen mensajes de forma simultánea sin que se bloqueen entre sí.
 
El servidor espera recibir mensajes serializados en JSON con la siguiente estructura:
 
```json
{
  "group": "<nombre del grupo>",
  "payload": "<mensaje>"
}
```
 
Si el mensaje recibido no tiene exactamente esos dos campos, o no es JSON válido, el servidor lo rechaza mostrando un aviso de mensaje mal formateado.
 
### ¿Qué es PacketSender y para qué lo usamos?
 
PacketSender es una herramienta gráfica que permite enviar paquetes TCP y UDP de forma manual, sin necesidad de escribir un cliente. Lo usamos en este punto para verificar que el servidor funciona correctamente antes de programar nuestro propio cliente en el Punto 3. Es útil para hacer pruebas rápidas y depurar el comportamiento del servidor de forma aislada.
 
En Linux se utiliza como un AppImage, que es un formato de distribución de aplicaciones que no requiere instalación: simplemente se le dan permisos de ejecución y se corre directamente.
 
### Procedimiento realizado
 
**1. Ejecución del servidor**
 
Se ejecutó el script `server.py` desde la terminal con el comando:
 
```bash
python3 server.py
```
 
El servidor quedó escuchando conexiones entrantes en todas las interfaces de red (`0.0.0.0`) en el puerto `5000`, mostrando el siguiente mensaje de confirmación:
 
```
Server listening on 0.0.0.0:5000
```
 
**2. Configuración y envío desde PacketSender**
 
Se abrió PacketSender y se configuraron los siguientes parámetros:

![PacketSender enviando el mensaje](assets/captura_packetsender.png)
 
- **Address:** `127.0.0.1` — la dirección loopback, que representa la propia máquina. Al ser cliente y servidor en la misma computadora, usamos esta dirección para que el paquete no salga a la red sino que se dirija localmente.
- **Port:** `5000` — el mismo puerto en el que el servidor está escuchando.
- **Protocolo:** `TCP`
- **Campo ASCII:** el mensaje JSON con el formato que el servidor espera:
```
{"group": "Latency_Killers2.0", "payload": "hola server"}
```
 
- Se activó la opción **Persistent TCP** para mantener la conexión abierta entre envíos, evitando que se abra y cierre una conexión TCP nueva en cada mensaje.
Luego se clickeó **Send**.
 
**3. Verificación en el servidor**
 
Al recibir el mensaje, el servidor mostró en la terminal:
 
![Terminal del servidor](assets/captura_servidor.png)
 
Esto confirma que:
- La conexión TCP fue establecida correctamente.
- El mensaje JSON fue recibido y deserializado sin errores.
- Los campos `group` y `payload` fueron extraídos e impresos correctamente.
- Al cerrar la conexión desde PacketSender, el servidor detectó la desconexión y cerró el hilo correspondiente.
 
## Punto 3 — Cliente TCP con serialización JSON
 
### ¿Que se hizo?
 
El cliente provisto por la cátedra tenía dos problemas: enviaba un mensaje hardcodeado con campos incorrectos (`nombre` y `que_digo`) que el servidor no reconoce, y se cerraba inmediatamente después de enviarlo. El objetivo de este punto es modificarlo para que sea interactivo y serialice los mensajes en el formato correcto que el servidor espera.
 
### Modificaciones realizadas al cliente
 
El cliente final cumple con los tres requisitos del punto:
 
**a) Configuración de IP y puerto**
 
La IP y el puerto del servidor se definen al inicio del script y se usan para establecer la conexión TCP:
 
```python
HOST = "127.0.0.1"
PORT = 5000
 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
```
 
Se usa `127.0.0.1` porque cliente y servidor corren en la misma máquina. En un escenario real se reemplazaría por la IP del servidor remoto.
 
**b) Serialización en el formato correcto**
 
Antes de enviar cada mensaje, se construye un diccionario Python con los campos `group` y `payload` que el servidor espera, y se serializa a JSON con `json.dumps()`. Luego se codifica a bytes UTF-8 para poder transmitirlo por el socket:
 
```python
message = {
    "group": GROUP,
    "payload": payload
}
client.sendall(json.dumps(message).encode("utf-8"))
```
 
**c) Consola interactiva**
 
El cliente entra en un loop que le pide al usuario un mensaje por consola en cada iteración. El loop continúa hasta que el usuario escribe `salir` o interrumpe con `Ctrl+C`:
 
```python
while True:
    payload = input("Mensaje: ")
    if payload.lower() == "salir":
        break
```
 
### Código completo del cliente
 
```python
import socket
import json
 
HOST = "127.0.0.1"
PORT = 5000
 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print(f"Conectado al servidor {HOST}:{PORT}")
 
GROUP = input("Ingresa el nombre de tu grupo: ")
 
try:
    while True:
        payload = input("Mensaje: ")
        if payload.lower() == "salir":
            break
 
        message = {
            "group": GROUP,
            "payload": payload
        }
 
        client.sendall(json.dumps(message).encode("utf-8"))
 
except KeyboardInterrupt:
    print("\nCerrando cliente...")
 
finally:
    client.close()
    print("Conexión cerrada.")
```
 
### Procedimiento realizado
 
Se abrieron dos terminales. En la primera se ejecutó el servidor:
 
```bash
python3 server.py
```
 
En la segunda se ejecutó el cliente:
 
```bash
python3 client.py
```
 
El cliente solicitó el nombre del grupo y luego permitió enviar mensajes de forma continua. Cada mensaje fue serializado a JSON y enviado al servidor por TCP. Al escribir `salir`, el cliente cerró la conexión correctamente.
 
### Verificación
 
En la terminal del servidor se pudo observar la recepción correcta de cada mensaje enviado desde el cliente, confirmando que la serialización y la transmisión funcionaron correctamente.
 
### Capturas de pantalla
 
**Captura 1 — Terminal del cliente enviando mensajes:**
 
![Terminal del cliente](assets/captura_cliente.png)
 
**Captura 2 — Terminal del servidor recibiendo los mensajes:**
 
![Terminal del servidor punto 3](assets/captura_servidor_p3.png)
