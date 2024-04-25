# Implementing face recognition using Functions-as-a-Service
## El objetivo de la practica:
El objetivo de esta práctica es desplegar y implementar funciones de reconocimiento facial utilizando Functions-as-a-Service (FaaS) con OpenFaaS y Kubernetes. Esta función debe ser capaz de recibir una imagen como entrada, detectar los rostros presentes en la imagen y devolver la imagen con los rostros detectados enmarcados en un rectángulo. Para ver la descripción, haga clic [aquí](https://github.com/pnovoa/cc2324/blob/main/practice2/REAME.md).

## Los requisitos  de práctica:   
Instala minikube ([ver sesión 4](https://github.com/pnovoa/cc2324/blob/main/session4/README.md#Kubernetes)).  
Instala [arkade](https://github.com/alexellis/arkade).  
Instala [OpenFaaS en Kubernetes](https://github.com/pnovoa/cc2324/blob/main/session7/README.md) usando arkade.   

## Pasos para implementar las funciones disponibles de OpenFaas:
Para hacerlo, debemos seguir los siguientes pasos y ejecutar los comandos en Git Bash abierto como administrador  
~~~
minikube start
~~~
Usando este comando, se inicia un clúster Kubernetes local y se crea un entorno de desarrollo de aplicaciones Kubernetes.  
  
![minikube start](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/0ef07ed3-6012-4137-8c0b-274889558c59)

~~~
minikube status
~~~  
Esto nos permite ver el estado del clúster que hemos creado.  

![image](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/115a38cf-b77a-4589-a0fc-65f82cd54356)

Después de iniciar el clúster, necesitaremos una herramienta de línea de comandos que facilite la instalación y gestión de aplicaciones en Kubernetes. Esa herramienta es Arkade. Con el siguiente comando, podemos descargarlo e instalarlo usando el script de instalación.  
~~~ 
curl -kksLS https://get.arkade.dev | sh    to install arkade 
~~~

![install arkade](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/3dc6135c-ffee-453b-8453-1bcde5afdd40)

  
Ahora, con la ayuda de Arkade, podemos descargar OpenFaaS, que es una plataforma FaaS que facilita el despliegue de funciones sin servidor en Kubernetes.  
~~~
arkade install openfaas
~~~

![install openfaas using arkade](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/67fe5c44-7091-45f2-b656-bf9838d4acd4)  

Una vez que la instalación haya finalizado, recibirás los comandos que necesitas ejecutar para iniciar sesión y acceder al servicio de puerta de enlace de OpenFaaS en Kubernetes.  
~~~
=======================================================================
= OpenFaaS has been installed.                                        =
=======================================================================

# Get the faas-cli
curl -SLsf https://cli.openfaas.com | sudo sh

# Forward the gateway to your machine
kubectl rollout status -n openfaas deploy/gateway
kubectl port-forward -n openfaas svc/gateway 8080:8080 &

# If basic auth is enabled, you can now log into your gateway:
PASSWORD=$(kubectl get secret -n openfaas basic-auth -o jsonpath="{.data.basic-auth-password}" | base64 --decode; echo)
echo -n $PASSWORD | faas-cli login --username admin --password-stdin
~~~

The `kubectl rollout status` command checks that all the containers in the core OpenFaaS stack have started and are healthy.

The `kubectl port-forward` command securely forwards a connection to the OpenFaaS Gateway service within your cluster to your laptop on port 8080. It will remain open for as long as the process is running, so if it appears to be inaccessible later on, just run this command again.

The `faas-cli` login command and preceding line populate the PASSWORD environment variable. You can use this to get the password to open the UI at any time


Con estos pasos, hemos logrado instalar y configurar OpenFaaS en nuestro clúster Kubernetes. Después de esto, podemos desplegar y controlar funciones sin servidor, y eso es lo que haremos en el siguiente paso  

Con este comando, podemos acceder a todas las funciones que tienen relación con la face 
~~~
faas-cli store list | grep face
~~~
![image](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/e75404e5-d26f-443d-9f0a-f0b0b686c28e)  

Lo que vamos a usar son face-detect-pigo y face-detect-openvc. Podemos ver sus detalles ejecutando el siguiente comando:  
~~~
faas-cli store inspect face-detect-pigo 
y  
faas-cli store inspect face-detect-openvc
~~~ 
Aquí está el resultado, que es una descripción del funcionamiento de cada función.  
  
![inspect face-detect-opencv](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/2d8e67fd-58ba-4083-8d3f-94f06af27441)  

![inspect face-detect-opencv](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/41f76538-594a-4964-aa5f-5536395cb04f)  
  

Para implementar estas funciones, se utilizan los siguientes comandos:
~~~
faas-cli store deploy face-detect-pigo
y
faas-cli store deploy face-detect-picv
~~~

![face-detect functions in openfaas](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/ce8267ee-66ca-47ff-ab43-46e9ead5958e)

Ahora, para invocar las funciones, necesitamos estos comandos:  
~~~
curl -d https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCdio_Sf9aON6NjLHo5fXjG1HNZzWCaTsUjQ http://127.0.0.1:8080/function/face-detect-pigo -o face-detect-pigo.png

curl -d https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCdio_Sf9aON6NjLHo5fXjG1HNZzWCaTsUjQ http://127.0.0.1:8080/function/face-detect-opencv -o face-detect-opencv.png
~~~
  
Se pasa el enlace de la foto que se desea usar, la URL de nuestra función y el nombre del archivo de salida, que en este caso son  face-detect-pigo.png y face-detect-opencv.png.



![test-opencv](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/da0d8b75-366f-444b-a000-f0d614f1a296)  

  face-detect-pigo.png    

    
![test-pigo](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/2b94cc6b-a36e-49f7-8791-1439816c425c)  

face-detect-opencv.png.  

## Desarrollar nuestra propias funcione de face-detection para FaaS: 

En nuestro caso, utilizaremos el lenguaje Python por su facilidad. Para hacerlo, usamos este comando 
~~~
 $ faas-cli new --lang python ilyas-facesdetection-python
~~~

 Esto nos crea 3 archivos que son :  
`ilyas-facesdetection-python/handler.py`: Este archivo contiene el código de la función que implemontamos en OpenFaaS.  

`ilyas-facesdetection-python/requirements.txt`: Este archivo especifica las dependencias de Python necesarias para ejecutar la función.  

`ilyas-facesdetection-python.yml`: Este archivo es el archivo de configuración específico para la función ilyas-facesdetection-python.  

La función de detección de faces se encuentra en el archivo handler.py  

Para compilar, enviar y implementar esta función, se utiliza el siguiente comando:  
~~~
$ faas-cli up -f ilyas-facesdetection-python.yml
~~~
Después de un tiempo, veremos nuestra imagen enviada a Docker Hub, como se muestra en la siguiente figura.

![docker hub](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/1fcbd7f0-ddc9-459a-85be-a7183b721c3b)  

tambien la podemos ver en  `http://127.0.0.1:8080/ui/`  

![ilyas-facedetec openfaasss](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/b44980b5-d20c-49e8-bdb4-ea3a7dfcf533)    

y abajo la el resultado final:  

![faces-detected](https://github.com/Ilyas-ZG/Cloud-Computing-Services-and-Applications/assets/116302871/05371aec-f223-412c-a2ae-e64d837e118e)



