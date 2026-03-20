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

A continuación se muestra la topología utilizada durante la simulación:

![Topología de red](./imagenes/topologia.png)

Nota: Esta imagen corresponde al esquema general armado en clase, donde se representan hosts, routers y sus interconexiones.

---

## Ejemplos de transmisión de paquetes

Durante la práctica se observaron distintos envíos de paquetes dirigidos a nuestra red 10.2, uno exitoso y otro fallido.

![Paquetes recibidos](./imagenes/paquetes.png)

En la imagen se pueden ver dos paquetes recibidos por la red destino.

En el primer caso, el paquete estaba dirigido a la IP 10.2.0.103. Si bien el paquete llegó a la red correspondiente, no existía ningún host con esa dirección IP, por lo que no pudo ser entregado. Esta situación generó un error de tipo "destination unreachable", simulando un comportamiento real de red ante destinos inexistentes.

En el segundo caso, el paquete enviado desde la IP 10.13.0.101 llegó correctamente al host 10.2.0.101, ya que dicha dirección existía dentro de la red. Esto permitió completar exitosamente la entrega del mensaje.

---

# Resolución de las preguntas

## a) Diferencia entre IP y MAC

---

## b) Uso del default gateway

---

## c) Ruteo hop-by-hop

---

## d) Reencapsulación de frames

---

## e) Función del TTL

---

# Conclusión

---