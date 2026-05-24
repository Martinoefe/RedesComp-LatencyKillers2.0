import socket
import json
from cryptography.fernet import Fernet

HOST = "127.0.0.1"
PORT = 5000
 

# Agrego cifrado para el payload. Punto 4.

#Primero cargo la clave secreta generada.
with open("secret.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
print(f"Conectado al servidor {HOST}:{PORT}")
 
GROUP = input("Ingresa el nombre de tu grupo: ")
 
try:
    while True:
        payload = input("Mensaje: ")
        if payload.lower() == "salir":
            break
 
        # Antes de enviar el payload, lo cifro utilizando la clave secreta.
        payloadCifrada = fernet.encrypt(payload.encode("utf-8")).decode("utf-8")

        message = {
            "group": GROUP,
            "payload": payloadCifrada
        }
 
        client.sendall(json.dumps(message).encode("utf-8"))
 
except KeyboardInterrupt:
    print("\nCerrando cliente...")
 
finally:
    client.close()
    print("Conexión cerrada.")