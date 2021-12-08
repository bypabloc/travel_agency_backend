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

## Comandos para arrancar el proyecto

    pipenv install
    pipenv shell
    python manage.py migrate
    python manage.py runserver

## Si el puerto esta ocupado, se puede usar el comando para liberarlo:
    lsof -t -i tcp:8000 | xargs kill -9

## Database structure

![Diagram class](/diagrams/diagram_class.svg)