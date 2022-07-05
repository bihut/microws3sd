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

### Clone the repository
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

API description through Swagger tool is comming. It will available in few days..


