## Entorno de desarrollo
    
    S.O.: Linux Ubuntu 20.04.3 LTS
    Python version: 3.8.10
    DataBase: psql (PostgreSQL) 14.1 (Ubuntu 14.1-2.pgdg20.04+1)

## Instalación
Antes de empezar con los comandos, se debe crear una base de datos.
Nombrela como ud desee, puede copiar el archivo ".env.example" y renombrarlo a ".env"
A continuación, cambie los valores de la base de datos en el archivo ".env"
Luego puede proseguir con los comandos de instalación.

## Tambien debe tener previamente instalado pipenv, sino lo tiene puede hacerlo con el sig comando:
    pip install pipenv

## Comandos para arrancar el contenedor:
    sudo docker-compose build --no-cache
    sudo docker-compose up -d --build --remove-orphans
    sudo docker-compose exec web python manage.py migrate --noinput

## Nota: 

### Comandos docker
    sudo docker-compose down
    sudo docker rm -f $(docker ps -a -q)
    sudo docker rmi -f $(docker images -aq)
    sudo docker volume rm $(docker volume ls -q)

## Si el puerto esta ocupado, se puede usar el comando para liberarlo:
    lsof -t -i tcp:8000 | xargs kill -9

## Postman Collection
![Archivo .json](/assets/postman_collection.json)

## Database structure
![Diagram class](/assets/diagrams/diagram_class.svg)