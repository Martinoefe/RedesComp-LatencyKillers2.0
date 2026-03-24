# Trabajo Práctico N°1 – Redes de Computadoras

## Integrantes
- Antonino, Tadeo - tadeo.antonino@mi.unc.edu.ar
- Quintana, Ignacio Agustin - ignacio.agustin.quintana@mi.unc.edu.ar
- Fioramonti, Martino - martino.fioramonti@mi.unc.edu.ar

## Fecha
*26/03/26*

---

# Parte 1: Simulación de envío de paquetes, ARP y ruteo

## Descripción general

En este trabajo práctico se simuló el envío de paquetes entre distintos hosts pertenecientes a diferentes redes. Para ello, se construyó una topología con múltiples LAN conectadas mediante routers, permitiendo observar el comportamiento del ruteo, la resolución ARP y el encapsulamiento de paquetes.

---

## Topología de red

Para la simulación usamos la siguiente topología:

![Topología de red](./imagenes/topologia.png)


---

## Ejemplos de transmisión de paquetes

Durante la práctica se observaron distintos envíos de paquetes dirigidos a nuestra red 10.2, uno fue exitoso y otro fallido.

![Paquetes recibidos](./imagenes/paquetes.png)

En la imagen se pueden ver dos paquetes recibidos por la red destino.

En el primer caso, el paquete estaba dirigido a la IP 10.2.0.103. Si bien el paquete llegó a la red correspondiente, no existía ningún host con esa dirección IP, por lo que no pudo ser entregado. Esta situación generó un error de tipo "destination unreachable", simulando un comportamiento real de red ante destinos inexistentes.

En el segundo caso, el paquete enviado desde la IP 10.13.0.101 llegó correctamente al host 10.2.0.101, ya que dicha dirección existía dentro de la red. Esto permitió completar exitosamente la entrega del mensaje.

---

# Resolución de las preguntas

## a) Diferencia entre IP y MAC

La **dirección IP** es un identificador lógico que sirve para ubicar un dispositivo en una red y puede cambiar (similar a como funciona una dirección de una casa), mientras que la **dirección MAC** es un identificador físico único asignado al hardware de red (sería un DNI) que normalmente no cambia; básicamente la IP nos dice **dónde está el dispositivo**, y la MAC indica **qué dispositivo es** dentro de la red.

---

## b) Uso del default gateway

El **default gateway** se usa cuando un dispositivo quiere enviar datos a una dirección IP que **no está dentro de su misma red local**, como no sabe llegar directamente, le entrega el paquete al gateway (puede ser el router), que actúa como intermediario y se encarga de **buscar la mejor ruta hacia otras redes**. En nuestra simulación, eran los grupos del centro a los que les dabamos el papelito del paquete cuando el destino no eera de nuestro grupo, para que lo reenvíen por el camino correcto.

---

## c) Ruteo hop-by-hop

El **ruteo hop-by-hop** es el proceso por el cual un paquete de datos no conoce toda la ruta hasta su destino, sino que **va avanzando paso a paso**: cada router recibe el paquete, consulta su tabla de ruteo y decide cuál es el **siguiente hop**, y así sucesivamente hasta llegar al destino final.

---

## d) Reencapsulación de frames

La **reencapsulación de frames** ocurre en cada salto de una red cuando un paquete llega a un router, este **quita el frame original**, analiza el paquete IP para decidir el siguiente destino, y luego **lo vuelve a encapsular en un nuevo frame** con las direcciones MAC correspondientes al siguiente salto. Sería como actualizar el remitente y destinatario para el próximo nodo.

---

## e) Función del TTL

El **TTL (Time To Live)** es un valor que lleva cada paquete IP para evitar que circule infinitamente por la red: **se decrementa en 1 en cada salto** y, cuando llega a 0, el paquete se descarta. Su función es **prevenir bucles de ruteo** y congestión.

---

# Conclusión

Creemos que este tipo de simulación "analógica/física" es realmente muy intuitiva para ver y aprender como funcionan las redes reales, dado que nos permite seguir visualmente el camino entero que realiza un paquete desde su origen hasta su destino, y también nos permite ver que pasa en casos donde no hay tal destino. 
Pudimos aprender los conceptos de **default gateway**, **ruteo hop by hop**, **TTL**, **reencapsulación de frames** y la diferencia entre **IP** y **MAC**.

---