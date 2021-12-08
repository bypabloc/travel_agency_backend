## Entorno de desarrollo
    
    S.O.: Linux Ubuntu 20.04.3 LTS
    Python version: 3.8.10
    DB: psql (PostgreSQL) 14.1 (Ubuntu 14.1-2.pgdg20.04+1)

## Instalación
Antes de empezar con los comandos, se debe crear una base de datos.
Nombrela como ud desee, puede copiar el archivo ".env.example" y renombrarlo a ".env"
A continuación, cambie los valores de la base de datos en el archivo ".env"
Luego puede proseguir con los comandos de instalación.

## Comandos para arrancar el proyecto
    virtualenv -p python3 env
    . env/bin/activate

    pip install -r requirements.txt

    cd project/
    python3 manage.py migrate
    python3 manage.py runserver

## Si el puerto esta ocupado, se puede usar el comando para liberarlo:
    lsof -t -i tcp:8000 | xargs kill -9

## Database structure

![Diagram class](/diagrams/diagram_class.svg)