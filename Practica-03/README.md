# Procesamiento y minería de datos en Big Data con Spark sobre plataformas Cloud
## El objetivo de la practica:
Esta práctica se enfoca en el uso de técnicas de procesamiento de grandes volúmenes de datos para resolver un problema de clasificación, específicamente
utilizando el conjunto de [Celestial Objects Dataset](https://www.kaggle.com/datasets/hari31416/celestialclassify) que se puede encontrar en Kaggle, mediante el desarrollo de modelos con la biblioteca MLLib de Spark. 
Vamos a ver la construcción y despliegue de imágenes Docker para un clúster Spark, la ejecución de scripts para entrenar modelos de clasificación con Spark MLlib,
y la utilización de un shell interactivo de PySpark para optimizar los modelos en tiempo real.

## Processus de déploiement et d'exécution de Spark avec Docker et Spark MLlib
### Paso 01
En el primer paso, primero debemos construir una imagen Docker para el nodo master y otro para los nodos worker que contengan Spark con la versión específica,
como en nuestro caso 3.5.1. Esto se hace utilizando los archivos [Dockerfile.master](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/blob/main/Practica-03/Dockerfile.master) y [Dockerfile.worker](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/blob/main/Practica-03/Dockerfile.worker) que están presentes en la carpeta, de esta manera podemos 
desplegar estas imágenes en un entorno compatible con Docker.
~~~
docker build -f Dockerfile.master -t myspark-master:3.5.1 .
docker build -f Dockerfile.worker -t myspark:3.5.1 .
~~~

![creat imagen ](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/2bafdf08-3745-4bcb-b41c-cbb30070241b)

### Paso 02
~~~
docker compose -d up
~~~
   
Aranca los contenedores definidos en [docker-compose.yml](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/blob/main/Practica-03/docker-compose.yml), en nuestro caso spark-master, 
spark-worker-a y spark-worker-b.
El master es responsable de la gestión y distribución de los recursos y tareas.
El worker es el encargado de ejecutar las tareas solicitadas por el master y está configurado para utilizar los recursos definidos, como los CPU y la memoria ...
En el archivo [docker-compose.yml](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/blob/main/Practica-03/docker-compose.yml) se puede encontrar la configuración de estos servicios master y worker (imagen, puertos, dependencias, variables de entorno, volúmenes, etc.).
  
![docker compose up](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/db855d4a-6c65-4157-bffc-ca9161673604)  

### Paso 03
~~~
docker exec -it practica3spark-spark-master-1 bash
~~~
Al ejecutar este comando, se abre una sesión interactiva en el contenedor del nodo master.  
![open spart interactive session](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/6bd8ed40-560a-4e3a-b58a-3ed65631b042)  


### Paso 04
~~~
/bin/spark-submit /opt/spark-apps/celestial_ms.py --output /opt/spark-data/out --input /opt/spark-data/medium_celestial.csv
~~~

Este comando coloca el script celestial_ms.py en Spark y utiliza el archivo medium_celestial.csv como entrada, especificando el directorio de salida como out.  
~~~
./bin/spark-submit /opt/spark-apps/celestial_ms.py --output /opt/spark-data/out --input /opt/spark-data/extra_small_celestial.csv
~~~

  
Lo mismo para este comando, se utiliza el script [celestial_ms.py](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/blob/main/Practica-03/apps/celestial_ms.py) para ejecutar los decision tree de decisiones y random forest utilizando Spark MLlib, 
pero esta vez se utiliza el archivo [extra_small_celestial.csv](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/blob/main/Practica-03/data/extra_small_celestial.csv) como entrada y se especifica el directorio de salida como out. Debido a que el primer archivo 
contiene muchos datos y mi PC no es lo suficientemente potente, lo probamos con [extra_small_celestial.csv](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/blob/main/Practica-03/data/extra_small_celestial.csv). Esto nos genera y guarda los dos modelos de decision tree
y random forest con la Evaluación de los modelos que se encuentra en params.json en ambos modelos. En este caso, la precisión del decesion tree es "AUC": 0.90, y para el random forest es "AUC": 0.97.
  
![output file](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/8deea35a-656f-4eaf-8bbf-04fb7aa58ee2)
___
También podemos usar la terminal de Spark para escribir nuestro código Python en la sesión interactiva, lo que nos permite optimizar y ver el rendimiento del modelo en tiempo real para realizar cambios y procesar más datos y realizar pruebas paso a paso.

Usamos

~~~
 /opt/spark/bin/pyspark --master spark://0.0.0.0:7077.
~~~

Con este comando, iniciamos un shell interactivo de PySpark para trabajar con Python utilizando la interfaz de línea de comandos. Especificamos la ubicación donde está instalado PySpark y la dirección junto con el puerto del master Spark, en nuestro caso, 0.0.0.0:7077.

Después de eso, obtenemos mejores parámetros y optimizaciones que podemos modificar en el archivo celestial_ms.py y guardarlo para entrenar nuestro modelo.





  
