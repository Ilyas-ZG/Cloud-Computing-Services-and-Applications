## Senario 01 : Pequeña empresa, grupo de usuarios pequeño:
Diseño y despliegue de un servicio Owncloud basado en contenedores según la arquitectura descrita en el Escenario 1.
En particular, se requiere que este servicio incluya, al menos, 4 microservicios:  
Servicio web ownCloud  
MariaDB  
Redis  
LDAP (autenticación de usuarios)  

### Arquitectura cloud propuesta:   
Una máquina ejecutando la aplicación: la web, el servidor de BD y almacenamiento local. Otra máquina prestando el servicio de autenticación a través de LDAP.
Este diagrama representaría la arquitectura propuesta:  

![arquitectura 01](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/8b1b02ed-8512-4542-b94e-58f60b600bff)  



### Services usados :  
Esta sección define los diferentes servicios de Docker que se implementarán.


#### Owncloud:   
Servicio OwnCloud que depende de MariaDB y Redis. Utiliza el volumen de archivos para almacenar datos.
Se refiere a especificar la imagen de Docker que se utilizará para crear el servicio OwnCloud.  
**Container_name**: owncloud_server: Es el nombre que se le da al contenedor Docker que ejecutará OwnCloud. Permite identificar y referenciar específicamente este contenedor dentro del sistema.  
**Restart** : always: Indica a Docker que debe reiniciar automáticamente el contenedor OwnCloud en caso de que se detenga por cualquier motivo.
**depends_on**: [mariadb, redis]: Especifica que el servicio OwnCloud depende de los servicios MariaDB (base de datos) y Redis (cache). Esto asegura que estos servicios se inicien antes que OwnCloud.  
**Environment**: Sección donde se configuran las variables de entorno necesarias para OwnCloud. Estas variables son esenciales para la configuración y el correcto funcionamiento de la aplicación OwnCloud.  
**healthcheck** : Esta sección define una prueba de salud para el contenedor OwnCloud. Verificará cada 30 segundos que el contenedor esté funcionando correctamente ejecutando el comando /usr/bin/healthcheck.

#### Mariadb:  
![image](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/47d91a94-669d-47fe-85a6-3eb7f9820bc0)  


Servicio MariaDB para la base de datos OwnCloud. Utiliza el volumen mysql para almacenar datos de la base de datos MariaDB.  
En estas lineas se Especifica la imagen de Docker a utilizar para MariaDB, luego se Define el nombre del contenedor Docker para MariaDB.  
luego se Configura las variables de entorno para MariaDB y al final volumes: [mysql:/var/lib/mysql]: Monta el volumen mysql para almacenar los datos de la base de datos MariaDB


#### Redis:  
![image](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/c4cb2e09-a8b7-4946-b665-87157f8ae215)  

Servicio Redis para OwnCloud, utilizado como caché. Utiliza el volumen de Redis para almacenar datos de Redis.  
igual a los otros servisios se define la imagen y el nombre y con la ligna command: ["--databases", "1"] , se establece el comando inicial para Redis, en este caso, limitando el número de bases de datos a 1.

#### Openldap:  
![image](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/6e6a3381-57d1-43a0-b205-35336ec4943f)  
servicio OpenLDAP para el servicio de directorio LDAP. Configura certificados, base de datos LDAP, contraseña de administrador, etc.  
igual a los otros tambien , aqui usamos ports: ["389:389", "636:636"] donde se expone los puertos 389 y 636 del contenedor, que son los puertos estándar utilizados por LDAP para las conexione  
#### Phpldapadmin :  
![image](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/4ce7cb43-65ac-4637-b006-b0127dbe7162)  
Interface web pour gérer OpenLDAP. Dépend du service OpenLDAP.

Podremos iniciar sesión con las credenciales de administrador que hayamos definido en las variables de entorno del fichero .env, usadas en el fichero docker-compose.yml. En mi caso sería admin y admin.  
![image](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/c932b244-53f1-456b-8ee6-4a87e8bfe8b9)  

Con la terminal escribimos
~~~
docker compose up
~~~
 y en nuestro docker desktop vemos lo siguiente  
 ![senario 01 docker desctop running](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/62008536-b4fd-41cc-a138-5e27c2132f40)  
 
Después de añadir un grupo y un usuario que en nuestro caso es 'ilyas zgaoula' como se muestra en la siguiente figura  
![ldap groupe and user cration](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/34c2361a-6714-4cb9-979c-63f925bd7a03)  

Accedemos con la cuenta admin admin de owncloud   
Luego vamos a añadir el usuario 'ilyas zgaoula' en owncloud usando el user authentification ya instalada en onwcloud,y seguir los siguientes pasos:  
Vamos a configuración, Aplicaciones y agregamos LDAPIntegration, luego vamos a autenticación de usuario:  
![ldap user validation](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/670ce6a1-4527-403a-adc9-fd91fc8846a0)  
![user configuration 3 step](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/dc7f8218-d32a-42cf-828a-6577f375a05b)  

Después de acceder con la cuenta del usuario 'ilyas zgaoula' y lo asigné a un grupo que es owncloudusers como se muestra en la siguiente figura:  

![owncloud users](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/7ad80cd4-db7f-447c-b067-8412eec26ce7)  





## Senario 02 : 
Diseño y despliegue de un servicio Owncloud basado en contenedores, con alta disponibilidad e inspirado en la arquitectura descrita en el Escenario 2. En particular, se requiere que este servicio incluya:  
Balanceo de carga con HAProxy u otra herramienta
Servicio web ownCloud
MariaDB
Redis
LDAP (autenticación de usuarios)
Replicación de, al menos, uno de los microservicios anteriores (Servidor web, LDAP o MariaDB).  
![diagrama](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/4599dce1-1872-4137-974d-39372a77859c)   

Vamos a utilizar los mismos servicios que hemos utilizado anteriormente, pero esta vez con una duplicación del servidor OwnCloud. En este caso, tendremos ocserver1 y ocserver2, para dividir la carga y controlar el balance mediante HAProxy. El archivo que hemos agregado se puede ver a continuación.  
![image](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/e4eade60-d82f-441d-8d24-5cdd29dae79d)  

Accedemos a http://localhost:8404/ tenemos la siguiente figura:  
![hproxy](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/2f6c7330-5008-4af7-b02f-f2acbcc2392d)  
A continuación podemos ver todos los servicios levantados incluyendo lo de mariadb master y esclavo.  
![image](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/0dac5ee6-3a6f-4c88-81a5-7ecbb47a1e50)
 






