# Trabajo Práctico N°2 – Redes de Computadoras

## Integrantes

* Antonino, Tadeo - [tadeo.antonino@mi.unc.edu.ar](mailto:tadeo.antonino@mi.unc.edu.ar)
* Quintana, Ignacio Agustin - [ignacio.agustin.quintana@mi.unc.edu.ar](mailto:ignacio.agustin.quintana@mi.unc.edu.ar)
* Fioramonti, Martino - [martino.fioramonti@mi.unc.edu.ar](mailto:martino.fioramonti@mi.unc.edu.ar)

---

# Introducción
Este trabajo tiene como propósito central familiarizarse con la operación y gestión de servicios en entornos de virtualización y nube.

A través de este TP, se aborda la seguridad en las comunicaciones mediante el estudio del protocolo SSH y el uso de criptografía de clave pública. En la sección práctica, se requiere el montaje de servidores TCP, UDP y HTTP en máquinas virtuales, utilizando herramientas como netcat para establecer conexiones y Wireshark para capturar y analizar el tráfico. El trabajo finaliza con una reflexión sobre la confidencialidad, para verificar si el contenido de las comunicaciones puede ser descifrado o intervenido, lo que refuerza la comprensión de la seguridad en la infraestructura web actual.

---

# Objetivos
- Repasar los fundamentos de acceso a infraestructura virtualizada, comprendiendo cómo se interactúa con sistemas que no están físicamente presentes
- Tomar contacto con infraestructura desplegada en la nube, aprendiendo a gestionar recursos en entornos remotos
- Analizar el comportamiento de los protocolos de transporte (TCP/UDP) y de aplicación (HTTP), observando procesos como el handshake y el intercambio de datos
- Evaluar la confidencialidad en las redes, reflexionando sobre la visibilidad de los datos y la importancia del cifrado

---

## 1) Investigación conceptual


### SSH y que problema resuelve
SSH es un protocolo que utiliza el modelo cliente-servidor: el cliente SSH se ejecuta en la computadora local del usuario y el servidor SSH en la maquina remota a la que se desea acceder. SSH opera habitualmente sobre el protocolo de transporte TCP en el puerto 22 por defecto.
El principal problema que resuelve este protocolo, es el de la vulnerabilidad de las comunicaciones en redes no confiables. Los protocolos anteriores, enviaban la informacion entre cliente-servidor en texto plano, incluyendo usuarios y contraseñas. Esto implicaba que el usuario quedara expuesto a posibles ataques. 

SSH soluciona estas deficiencias mediante los siguientes mecanismos de seguridad:
- **Cifrado (Confidencialidad):** SSH cifra todos los datos transmitidos, haciendo que la información sea ilegible para cualquier tercero que intercepte la comunicación.
- **Autenticación fuerte:** Utiliza criptografía de clave pública (como RSA) para que el cliente pueda verificar que el servidor es realmente quien dice ser, y viceversa. Esto previene ataques de suplantación de identidad.
- **Integridad de los datos:** Garantiza que los mensajes no han sido alterados ni manipulados durante su tránsito por la red


### Cifrado vs Autenticación
La principal diferencia entre cifrado y autenticación es que la autenticación se concentra principalmente en la identidad de las entidades comunicantes y en validar que sean quienes dicen ser. Mientras que el cifrado se centra en la confidencialidad de los datos y en asegurar que solo los receptores autorizados puedan comprender el contenido transmitido, la autenticación busca confirmar el origen del mensaje para evitar la suplantación de identidad. Es importante destacar que el cifrado por sí solo no garantiza la autenticidad, ya que es posible recibir un mensaje secreto cuyo contenido haya sido modificado maliciosamente después de su creación sin que el receptor pueda detectarlo fácilmente. Por su parte, la autenticación implica a menudo la integridad de los datos, puesto que carece de sentido validar a un participante si el mensaje recibido ya no es el mismo que se envió originalmente. En la práctica de las comunicaciones modernas, estas herramientas se combinan para protegerse tanto de ataques pasivos, como la escucha no autorizada mediante el cifrado, como de ataques activos, como la falsificación de datos mediante mecanismos de autenticación. Así, mientras el cifrado transforma la información en un formato ininteligible para cualquier intruso, la autenticación utiliza elementos como contraseñas, firmas digitales o números distintivos para asegurar una interacción legítima entre las partes


### Claves publicas y privadas
Una clave pública y una clave privada son un par de claves matemáticamente relacionadas que se utilizan en la criptografía asimétrica para garantizar la seguridad de las comunicaciones. La clave pública, como su nombre lo indica, es de conocimiento general y puede ser distribuida a cualquier persona para que la utilice al cifrar mensajes dirigidos al dueño del par de claves o para verificar su firma digital. Por el contrario, la clave privada debe ser mantenida en estricto secreto por su creador, ya que es la única herramienta capaz de descifrar la información que fue protegida con su contraparte pública, asegurando así que solo el destinatario legítimo pueda acceder al contenido original

Este sistema permite que dos entidades se comuniquen de forma segura a través de una red sin necesidad de haber compartido previamente una clave secreta, resolviendo uno de los mayores problemas de la criptografía tradicional. Un aspecto fundamental de esta tecnología es que, aunque ambas claves están vinculadas mediante funciones matemáticas complejas, resulta computacionalmente imposible deducir o calcular la clave privada a partir de la clave pública conocida por todos. Gracias a esta propiedad, el sistema garantiza que cualquier usuario pueda obtener la clave pública de otro y enviarle información confidencial con la certeza de que nadie más, excepto el poseedor legítimo de la clave privada, podrá recuperar y leer el mensaje.


### ¿Porque debo protejer mi clave privada?
La clave privada no debe compartirse porque es el componente fundamental que garantiza tanto la confidencialidad como la identidad del propietario en un sistema de criptografía asimétrica. Al ser la única herramienta capaz de descifrar la información que ha sido protegida con su clave pública correspondiente, su divulgación permitiría que cualquier tercero interceptara y leyera mensajes privados destinados exclusivamente al dueño original. El secreto absoluto de esta clave es lo que asegura que solo el destinatario legítimo pueda acceder al contenido de la comunicación, manteniendo la privacidad del sistema.


Además, compartir la clave privada compromete totalmente la autenticación y la validez de las firmas digitales. Dado que la posesión de esta clave es lo que identifica de manera única a una entidad en la red, si un tercero la obtiene, podrá realizar un ataque de suplantación de identidad (impersonation), firmando documentos o accediendo a infraestructuras seguras como si fuera el usuario legítimo. En el momento en que una clave privada deja de ser secreta, la confianza en todo el par de claves se rompe, lo que obliga a revocar los certificados de seguridad existentes y a generar un nuevo par para restablecer la protección.

### SSH vs Contraseñas
Las claves SSH ofrecen varias ventajas fundamentales sobre el uso de contraseñas tradicionales, centrándose principalmente en una seguridad robusta y en la eficiencia operativa. A diferencia de las contraseñas, que suelen ser vulnerables a ataques de fuerza bruta o de diccionario por ser frecuentemente débiles o fáciles de adivinar, las claves SSH se basan en criptografía asimétrica, lo que las hace virtualmente imposibles de descifrar mediante métodos convencionales debido a su enorme complejidad matemática. Además, aunque SSH permite el envío de contraseñas de forma cifrada dentro de su canal seguro, el uso de pares de claves pública y privada proporciona una autenticación mucho más fuerte, ya que la clave privada nunca se transmite a través de la red, eliminando el riesgo de que la credencial secreta sea interceptada durante el tránsito.


Otra ventaja significativa es la comodidad y capacidad de automatización que permiten, facilitando el inicio de sesión remoto y la transferencia segura de archivos sin necesidad de intervención manual constante, lo cual es ideal para scripts y administración de infraestructura a gran escala. Desde el punto de vista de la gestión de identidades, las claves permiten un control de acceso más escalable: para revocar el acceso de un usuario, basta con eliminar su clave pública del servidor, evitando los peligros de seguridad asociados a las contraseñas compartidas que rara vez se cambian. En resumen, las claves SSH sustituyen el modelo de un "secreto compartido" por uno de criptografía de punto terminal, ofreciendo una defensa superior contra la suplantación de identidad y las intrusiones en redes no confiables.




### 2) Conexion por SSH
La primera vez que nos queriamos conectar nos tiro un error (desde Windows por lo menos)- 

Bad permissions. Try removing permissions for user: NT AUTHORITY\\Usuarios autentificados (S-1-5-11) on file D:/Descargas/pc3_key (1).pem.
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions for 'D:\\Descargas\\pc3_key (1).pem' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "D:\\Descargas\\pc3_key (1).pem": bad permissions
pc-alumnos-3@4.206.219.90: Permission denied (publickey).

El problema era que tenia permisos demasiados abiertas las KEY y SSH no me permitia usarlas por eso. 

Luego logramos hacer la conexión SSH con las VM.

### 3) Uso de Wireshark
Al analizar el tráfico con Wireshark nos dimos cuenta que no pudimos descifrar el contenido de los paquetes, esto es debido al uso de SSH el cual trabaja en dos pasos: primero se hace lo que se conoce como "handshake" en donde la VM y nuestra PC local acuerdan como se enviarán la información; en segundo lugar viene el cifrado donde la información se encripta de forma tal que solo nuestra PC local o la VM puedan saber desencriptar la información y leerla. Wireshark funciona como un interceptor que puede ver información como de donde salió el paquete pero no tiene la información necesaria para descifrarlo.

![PC3](/TP3/assets/ConexionPC3.jpeg)

---

![PC4](/TP3/assets/ConexionPC4.jpeg)

### 4) NetCat

Esta vez fue posible descifrar el contenido de los mensajes interceptados por Wireshark dada la ausencia de SSH que encripte los mismos. Esto nos hizo ver la importancia de usar herramientas de seguridad como SSH que nos ayudan a mantener la privacidad de nuestra información.

Acá se pueden ver los mensajes que enviamos a través del servidor y como el Wireshark los pudo leer.

![severPC3](/TP3/assets/chatServerPC3.jpeg)
![serverPC4](/TP3/assets/chatServerPC4.jpeg)

Y acá es donde se ve como Wireshark leyó el mensaje:

![mensaje_wireshark](/TP3/assets/Wireshark_conMensaje.jpeg)

Y esto es lo que detectó el Wireshark cuando agregamos el UDP:

![UDP](/TP3/assets/Wireshark_conMensaje_UDP.jpeg)

### 5) Trafico HTTP

Levantamos un HTML sencillo pero como el server usa protocolo HTTP y no HTTPS (S de Secure) es posible sufrir ataques del tipo man in the middle en el cual se intercepten, lean y modifiquen los paquetes porque estos no cuentan con ningún tipo de certificado de seguridad ni de integridad de datos que adviertan al usuario receptor de su modificación.

![HTML_Messi](/TP3/assets/HTML.jpeg)
![wireshark_HTML](/TP3/assets/ultimoWireshark.jpeg)

### 6) Video del hackeo al iPhone

En el video se ve como se aprovechan de una vulnerabilidad del sistema de pago sin contacto para robar U$D 10,000 de la tarjeta VISA vinculada al iPhone del sujeto.

El ataque es lo que en ciberseguridad se conoce como un ataque de man in the middle. Usando equipos especiales ocultos, los hackers interceptan la comunicación inalámbrica entre el celular de la víctima y un lector de tarjetas real, modificando los datos en tiempo real.

Apple tiene un sistema que permite pagar boleto de subte con el teléfono bloqueado, los atacantes se aprovechan de esta funcionalidad envíando una señal falsa al iPhone que le haga creer que está en una estación de subte para que pueda hacer el pago aun estando bloqueado.

Luego, proceden a engañar al iPhone haciendole creer que es una transacción de bajo valor por lo que no requiere verificación biométrica como usualmente se pide en transacciones grandes. Esto se logra cambiando un solo bit de la información.

Por último, modifican el mensaje de respuesta que el iPhone le envía al lector de tarjetas, diciéndole falsamente que el usuario "ya verificó la compra" en su teléfono. Con esto el cobro se aprueba.


En los Trabajos Prácticos realizados hasta el momento trabajamos con conceptos relacionados a los que se muestran en el video:

TP1 - Modificación de bits en el Payload: En la segunda parte del TP1 experimentamos con la inyección de errores modificando bits de los paquetes. El ataque del video se basa exactamente en esto: los atacantes interceptan el paquete de datos y cambian bits específicos como dijimos antes.

TP2 - Análisis de tráfico: El TP2 se centra en capturar y analizar el comportamiento del tráfico. En el video, los investigadores relatan que fueron a una estación de metro con sus notebooks para "escanear las señales" y leer el código que enviaban los molinetes, lo cual es equivalente a lo que nosotors hicimos analizando paquetes.
TP3 - man in the middle y HTTP: En el TP3 vimos que el tráfico HTTP viaja en texto plano y puede ser intervenido , a diferencia del tráfico cifrado de SSH. El ataque al youtuber del video es un man in the middle donde interceptan la señal NFC porque la información viaja sin cifrar por motivos de compatibilidad.
TP3 - Cifrado y Autenticación: El TP3 nos pide investigar la diferencia entre estos conceptos. En el video se ve que aunque los datos del lector viajan sin cifrar, el sistema confía en la autenticación mediante firmas criptográficas asimétricas. El hackeo funciona justamente porque la configuración de Visa omite ese paso de autenticación al estar en "modo transporte".