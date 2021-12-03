## Environment development
    
    S.O.: Linux Ubuntu 20.04.3 LTS
    Python version: 3.8.10
    DB: psql (PostgreSQL) 14.1 (Ubuntu 14.1-2.pgdg20.04+1)

## Command run project
    virtualenv -p python3 env
    . env/bin/activate

    pip install -r requirements.txt

    cd project/
    python3 manage.py migrate
    python3 manage.py runserver

## Kill port
    lsof -t -i tcp:8000 | xargs kill -9

## Database structure

![Diagram class](/diagrams/diagram_class.svg)