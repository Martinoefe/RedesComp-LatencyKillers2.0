# Trabajo Práctico N°5 – Redes de Computadoras
 
## Integrantes

* Antonino, Tadeo - [tadeo.antonino@mi.unc.edu.ar](mailto:tadeo.antonino@mi.unc.edu.ar)
* Quintana, Ignacio Agustin - [ignacio.agustin.quintana@mi.unc.edu.ar](mailto:ignacio.agustin.quintana@mi.unc.edu.ar)
* Fioramonti, Martino - [martino.fioramonti@mi.unc.edu.ar](mailto:martino.fioramonti@mi.unc.edu.ar)

---

## 1) Reconocimiento de arquitectura 

-Firewall: Es la primera línea de defensa. Su función es bloquear el tráfico malicioso. Se ubica entre la capa de Internet y la capa de Transporte (puede subir a la capa de Aplicación). Si faltara, el tráfico malicioso saturaría instantáneamente los recursos de los servidores, provocando una caída total por ataques DDoS.

-Load Balancer: Se encarga de distribuir el tráfico a múltiples instancias de cómputo. Opera en la capa de Transporte o en la capa de Aplicación. Si faltara, todo el tráfico caería sobre un único servidor, no se podría escalar horizontalmente y el sistema colapsaría.

-Queue: Son buffers que previenen caídas durante sobrecargas o picos. Pertenece a la capa de Aplicación. Si faltara, los picos repentinos de tráfico saturarían los hilos de ejecución de los servidores, generando errores de timeout y fallas por sobrecarga.

-Compute: Nodo. Solicita procesos. Se encuentra en la capa de Aplicación. Si faltara, la arquitectura carecería de capacidad de cómputo, no existiría un entorno para ejecutar el código ni procesar la lógica de negocio.

-Serverless Function: Escala automáticamente con el tráfico. Es de bajo mantenimiento aunque tiene alto costo por proceso completado. Está situado en la capa de Aplicación. Si faltara, se perdería la capacidad de absorber ráfagas masivas de eventos aislados de forma inmediata sin pagar por servidores encendidos las 24 horas.

-SQL DB: Base de datos que opera como destino para tráfico de READ/WRITE/SEARCH. Corresponde a la capa de Aplicación. Si faltara, no habría un sistema centralizado, persistente y relacional para garantizar la consistencia de los datos críticos y las transacciones.

-NoSQL: Base de datos más rápida para READ/WRITE pero que no puede manejar SEARCH. Se localiza en la capa de Aplicación. Si faltara, las operaciones masivas de READ/WRITE rápida sobrecargarían la base de datos relacional principal, ralentizando todo el sitio.

-Cache: Se usa para bajar la carga de las DB. Se posiciona en la capa de Aplicación. Si faltara, cada consulta idéntica impactaría en los discos de las bases de datos, degradando severamente el tiempo de respuesta del sistema bajo uso concurrente.

-CDN: Content Delivery Network. Procesa el tráfico del tipo STATIC. Se clasifica dentro de la capa de Aplicación. Si faltara, el tráfico estático inundaría los servidores de backend, consumiendo su CPU y ancho de banda innecesariamente en entregar simples imágenes.

-Storage: Es el destino del tráfico del tipo STATIC/UPLOAD. Está asignado a la capa de Aplicación. Si faltara, los archivos subidos por los usuarios llenarían rápidamente el disco local del servidor de aplicación, provocando que el sistema operativo falle por falta de espacio.

-Search Engine: Alternativa a una SQL DB para procesar peticiones SEARCH de manera más rápida. Se integra en la capa de Aplicación. Si faltara, las búsquedas complejas por texto requerirían consultas SQL extremadamente pesadas, indexando tablas enteras y congelando la base de datos.

-Réplica: Descarga tráfico READ de la DB maestra. Hace su trabajo en la capa de Aplicación. Si faltara, todo el tráfico de consulta golpearía al nodo maestro de la base de datos, bloqueando las operaciones de escritura y pausando la aplicación.

Es importante destacar que muchos de los componentes operan en la capa de Aplicación porque el propósito de las capas inferiores en el modelo TCP/IP es mover paquetes de datos de un punto A a un punto B de forma segura y confiable, sin importar qué contienen esos paquetes adentro.

A la capa de Internet (IP) solo le importa la dirección de destino.

A la capa de Transporte (TCP) solo le importa que los paquetes lleguen completos y en orden usando puertos.

Una vez que TCP cumplió su trabajo y ordenó los paquetes, se los entrega al sistema operativo. A partir de ahí todo lo que sucede con esos datos es tarea exclusiva de la capa de Aplicación.


---



## 2) Tipos de Tráfico

| Tipo de tráfico | Ejemplo real | Componente recomendado | Riesgo si se procesa incorrectamente |
| --- | --- | --- | --- |
| **STATIC** | Archivos CSS de estilos, logotipos o imágenes de la interfaz, y scripts fijos de JavaScript. | **CDN** o **Storage** | Desperdicio innecesario de la capacidad de cómputo del servidor de aplicaciones (*Compute*), aumentando costos y ralentizando la carga general del sitio. |
| **READ** | Consultar el perfil público de un usuario, listar los productos disponibles en una tienda o leer un artículo de noticias. | **Cache** (para datos frecuentes) y **Réplicas de lectura** de la base de datos. | Saturación y cuello de botella en los discos de la base de datos principal, provocando demoras extremas en todas las consultas del sistema. |
| **WRITE** | Registrar un nuevo usuario, realizar una compra en el carrito, publicar un comentario o actualizar una contraseña. | **SQL DB** o **NoSQL DB** (según la estructura). | Pérdida de datos transaccionales críticos del negocio, inconsistencias en el sistema o bloqueos concurrentes en las tablas de almacenamiento. |
| **UPLOAD** | Subir una foto de perfil en formato JPG, adjuntar un documento PDF para una tarea o cargar un archivo de video. | **Storage** (Almacenamiento de objetos). | Llenado rápido del disco de almacenamiento local del servidor de aplicaciones, provocando fallas imprevistas y el colapso del sistema operativo. |
| **SEARCH** | Buscar un artículo escribiendo palabras clave en la barra de búsqueda (ej: "zapatillas deportivas impermeables"). | **Search Engine** dedicado. | Ejecución de consultas de texto (*queries*) sumamente ineficientes en la base de datos relacional, forzando escaneos completos de tablas que congelan el servicio. |
| **MALICIOUS** | Ataques de denegación de servicio distribuido (DDoS), escaneos automatizados de vulnerabilidades o inyecciones de código. | **Firewall** | Consumo total e inmediato del ancho de banda y de los hilos de procesamiento, dejando la infraestructura completamente inaccesible para los usuarios legítimos. |


---


## 3) Test de Queues

Al aumentar fuertemente el traffic rate notamos que luego de la queue la cantidad de "bolitas" disminuye drásticamente, lo cual es acorde a la función de la queue que, como se mencionó antes, opera como buffer.

![queue1](assets/queue_high_rate.png)

Luego si bajamos el traffic rate a 0 instantáneamente observamos como desde la queue hacia la compute solo pasa el tráfico remanente que quedó buffereado antes.

![queue2](assets/queue_0_rate.png)


---


## 4) Infraestructura mínima

Armamos una infraestructura mínima que consta de un firewall para controlar el tráfico malicioso, un load balancer (en realidad como usamos un solo compute no lo queríamos poner, pero no nos deja pasar del firewall directamente a compute), un compute, una CDN que procesa el tráfico estático, un storage para uploads, un search para search valga la redundancia, y una NoSQL para las read y write.

![arq_inicial](assets/arq_inicial.png)

De este modo, comenzamos con el siguiente presupuesto:

![budget](assets/presupuesto_inicial.png)

Al comenzar la simulación con una bajo traffic rate se puede observar que la infraestructura es capaz de soportar la carga, como se ve en la imagen:

![tranquilo](assets/tranquilo.png)

Luego de aumentar el traffic rate a valores muy altos pudimos ver como el nodo compute colapsa, haciendo caer nuestra reputación casi al instante, como se puede observar en la imagen siguiente:

![colapsado](assets/colapsado.png)

Y la baja reputación:

![reputacion](assets/reputacion.png)


Entonces ¿Que sucedió realmente?

Al desarrollar una infraestructura sin mecanismos de optimización y desacoplamiento para el tráfico dinámico transaccional tales como queues o cachés, el aumento repentino del traffic rate hace colapsar el sistema, en particular el nodo compute, que no puede procesar tantas solicitudes tan rápido, llegando al 100% de sus capacidades rápidamente. 

Esto es claramente un problema de diseño, el núcleo dinámico de la red colapsó debido a una topología centralizada y síncrona. El simulador demuestra que el problema no se soluciona simplemente pagando por un componente de mayor "capacidad", sino modificando el diseño estructural para incorporar capas de caché y balanceo real que distribuyan el esfuerzo computacional. 


---


## 5) Escalabilidad y balanceo

