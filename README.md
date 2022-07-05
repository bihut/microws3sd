# μws3sd
**μWS3D** architecture enables the customization of 3D assets through a microservice architecture

The architecture has been implemented following a monolithic approach as well as microservice approach supported by 
Kubernetes technology. In addition, several test plan have been carried out to determine which 
implementation provides the better performance.

This repository guide through the installation process of both implementations.

## Pre-requisites before installing **μWS3D** (both implementations)

Both implementations haven been developed in Python, and tested in Ubuntu 20.04 and 21.10. All the code
has been implemented in Python, so there is no problem to deploy the system in other platforms as 
Windows or Macs. However, the different instructions described here to guide the installation process
are oriented for Linux users, especially Debian-based distros.

#### First of all, update and upgrade your system:
> sudo apt-get install update

> sudo apt-get install upgrade

#### Install the essentials
> sudo apt-get install build-essential
 
#### Install Python and pip (Python 3.9 is recommended)
>sudo apt install software-properties-common

> sudo add-apt-repository ppa:deadsnakes/ppa

> sudo apt install python3.9

> sudo apt install python3-pip 

#### Install MongoDB
> https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/

#### Download Blender
> https://www.blender.org/download/

#### Install Git
> sudo apt install git

#### Clone the repository
> git clone https://github.com/bihut/microws3sd.git
> Open the folder "microws3d"

## Monolithic Implementation

Monolithic implementation follows a traditional approach, so the deployment is quite very easy. Once you are located
in the "Monolithic" folder, just launch:

> pip install -r requirements

Once all the libraries have been installed, go to Monolithic/structure.json and set the parameters: database features, 
Blender location, etc.

Now you can run the back-end using:

> python app.py

You can start to use it using the different services (check them in the file app.py).

API description through Swagger tool is coming. It will be available in few days.

## Microservices Implementation
This implementation has been done using Docker and Kubernetes, specifically Minikube.
First of all, Docker and Minikube must be installed.

#### Install Docker
> https://docs.docker.com/engine/install/ubuntu/

#### Install Minikube
> https://minikube.sigs.k8s.io/docs/start/

Unlike the monolithic implementation, in this architecture the services are a set of PODs, where each one
contains a Docker image. 
## -----------------
Once Docker is installed, please pull the different images from the Docker Hub:
> docker pull 967111488415952/ws3d-blender

> docker pull 967111488415952/ws3d-utils

> docker pull 967111488415952/ws3d-assemblies

> docker pull 967111488415952/ws3d-textures

> docker pull 967111488415952/ws3d-animations

Modify the host to add your computer domain. First, get your private ip address (IPADDRESS)
> ipcofing

Modify your host:
> nano /etc/hosts

Add at the end of the file
> IPADDRESS ws3d.info

Launch minikube and the tunnel to ensure the forwarding:
> minikube start

In a different terminal:
> minikube tunnel

Go through all the folders inside Microservices and run the following commands to deploy the services and the Docker images
> kubectl apply -f animations-deployment.yml

> kubectl apply -f animations-service.yml

> kubectl apply -f assemblies-deployment.yml

> kubectl apply -f assemblies-service.yml

> kubectl apply -f blender-deployment.yml

> kubectl apply -f blender-service.yml

> kubectl apply -f textures-deployment.yml

> kubectl apply -f textures-service.yml

> kubectl apply -f utils-deployment.yml

> kubectl apply -f utils-service.yml

Now, go back to Microservices root folder to install the ingress:
> kubectl apply -f ws3d-ingressingress.yml

Now all is running, open the browser and type, for instance:
> http://ws3d.info/animations

If you see a JSON as response return, that means everything is working fine now!

## JMeter metrics
JMeterDataset contains all the metrics gathered during the tests done for 1, 3, 5, 10, 25, 50, 75, 100 and 200 users 
for both implementations. The data is categorized by implementation -> number of users --> type of data (aggregate, 
summary, table)