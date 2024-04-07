Senario 01 :
Pequeña empresa o departamento - grupo de usuarios pequeño

Diseño y despliegue de un servicio Owncloud basado en contenedores según la arquitectura descrita en el Escenario 1.
En particular, se requiere que este servicio incluya, al menos, 4 microservicios:
Servicio web ownCloud
MariaDB
Redis
LDAP (autenticación de usuarios)

Arquitectura cloud propuesta: 
Una máquina ejecutando la aplicación: la web, el servidor de BD y almacenamiento local. Otra máquina prestando el servicio de autenticación a través de LDAP.
Este diagrama representaría la arquitectura propuesta:
**************
PHOTO ARqUITECTURA 01 
**************

Services usados : 
Esta sección define los diferentes servicios de Docker que se implementarán.


owncloud: servicio OwnCloud que depende de MariaDB y Redis. Utiliza el volumen de archivos para almacenar datos.
 Se refiere a especificar la imagen de Docker que se utilizará para crear el servicio OwnCloud.
container_name: owncloud_server: Es el nombre que se le da al contenedor Docker que ejecutará OwnCloud. Permite identificar y referenciar específicamente este contenedor dentro del sistema.
restart: always: Indica a Docker que debe reiniciar automáticamente el contenedor OwnCloud en caso de que se detenga por cualquier motivo.
depends_on: [mariadb, redis]: Especifica que el servicio OwnCloud depende de los servicios MariaDB (base de datos) y Redis (cache). Esto asegura que estos servicios se inicien antes que OwnCloud.
environment: Sección donde se configuran las variables de entorno necesarias para OwnCloud. Estas variables son esenciales para la configuración y el correcto funcionamiento de la aplicación OwnCloud.
healthcheck: Esta sección define una prueba de salud para el contenedor OwnCloud. Verificará cada 30 segundos que el contenedor esté funcionando correctamente ejecutando el comando /usr/bin/healthcheck.

mariadb: Servicio MariaDB para la base de datos OwnCloud. Utiliza el volumen mysql para almacenar datos de la base de datos MariaDB.
En estas lineas se Especifica la imagen de Docker a utilizar para MariaDB, luego se Define el nombre del contenedor Docker para MariaDB. luego se Configura las variables de entorno para MariaDB y al final volumes: [mysql:/var/lib/mysql]: Monta el volumen mysql para almacenar los datos de la base de datos MariaDB


redis: Servicio Redis para OwnCloud, utilizado como caché. Utiliza el volumen de Redis para almacenar datos de Redis.
igual a los otros servisios se define la imagen y el nombre y con la ligna command: ["--databases", "1"] , se establece el comando inicial para Redis, en este caso, limitando el número de bases de datos a 1.

openldap: servicio OpenLDAP para el servicio de directorio LDAP. Configura certificados, base de datos LDAP, contraseña de administrador, etc.
igual a los otros tambien , aqui usamos ports: ["389:389", "636:636"] donde se expone los puertos 389 y 636 del contenedor, que son los puertos estándar utilizados por LDAP para las conexione
phpldapadmin : Interface web pour gérer OpenLDAP. Dépend du service OpenLDAP.



Podremos iniciar sesión con las credenciales de administrador que hayamos definido en las variables de entorno del fichero .env, usadas en el fichero docker-compose.yml. En mi caso sería admin y admin.



mainteenat pour configuer le LDAP autentification , on dois suivre les etapes suivantes : 
nous allons sur setting , Apps, et on ajoute LDAPIntegration , apres on va sur user uthentication 



Senario 02:
Diseño y despliegue de un servicio Owncloud basado en contenedores, con alta disponibilidad e inspirado en la arquitectura descrita en el Escenario 2. En particular, 
se requiere que este servicio incluya:

Balanceo de carga con HAProxy u otra herramienta
Servicio web ownCloud
MariaDB
Redis
LDAP (autenticación de usuarios)
Replicación de, al menos, uno de los microservicios anteriores (Servidor web, LDAP o MariaDB).