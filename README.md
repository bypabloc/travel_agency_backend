## Environment development
    
    S.O.: Linux Ubuntu 20.04
    Python version: 3.8.10

## Command run project
    virtualenv -p python3 env
    . env/bin/activate

    pip install -r requirements.txt

    cd project/
    python3 manage.py migrate
    python3 manage.py runserver

## Database structure

![Diagram class](/diagrams/diagram_class.svg)