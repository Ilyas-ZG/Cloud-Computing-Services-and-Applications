# Implementing face recognition using Functions-as-a-Service
## El objetivo de la practica:
El objetivo de esta práctica es desplegar y implementar funciones de reconocimiento facial utilizando Functions-as-a-Service (FaaS) con OpenFaaS y Kubernetes. Esta función debe ser capaz de recibir una imagen como entrada, detectar los rostros presentes en la imagen y devolver la imagen con los rostros detectados enmarcados en un rectángulo.  

## Los requisitos  de práctica:   
Instala minikube ([ver sesión 4](https://github.com/pnovoa/cc2324/blob/main/session4/README.md#Kubernetes)).  
Instala [arkade](https://github.com/alexellis/arkade).  
Instala OpenFaaS en Kubernetes usando arkade.   

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

