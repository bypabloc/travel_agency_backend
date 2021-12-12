## Entorno de desarrollo

### docker --version
    Docker version 20.10.11, build dea9396

### docker-compose --version
    docker-compose version 1.27.4, build 40524192

## Instalación
Antes de empezar con los comandos, se debe crear una base de datos.
Nombrela como ud desee, puede copiar el archivo ".env.example" y renombrarlo a ".env"
A continuación, cambie los valores de la base de datos en el archivo ".env"
Luego puede proseguir con los comandos de instalación.

## Comandos para arrancar el contenedor:
    sudo docker-compose build --no-cache
    sudo docker-compose up -d --build --remove-orphans

## Nota, comandos docker: 

### Comandos para ver el log de un contenedor:
    sudo docker-compose logs -t -f web

### Comandos para bajar todos los contenedores:
    sudo docker-compose down

### Comandos para bajar todos los contenedores:
    sudo docker rm -f $(docker ps -a -q)

### Comandos para bajar todas las imagenes:
    sudo docker rmi -f $(docker images -aq)

### Comandos para bajar todos los volumenes:
    sudo docker volume rm $(docker volume ls -q)

## Si el puerto esta ocupado, se puede usar el comando para liberarlo:
    lsof -t -i tcp:8000 | xargs kill -9

## Postman Collection
[Archivo .json](/assets/postman_collection.json)

## Database structure
![Diagram class](/assets/diagrams/diagram_class.svg)