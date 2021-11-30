Create Project
    
    S.O.: Linux Ubuntu 20.04
    Python version: 3.8.10

## command code
    virtualenv -p python3 env
    . env/bin/activate

    pip install -r requirements.txt

    cd project/
    python3 manage.py migrate
    python3 manage.py runserver

## Estructura de la base de datos

![Diagram class](/diagrams/diagram_class.svg)