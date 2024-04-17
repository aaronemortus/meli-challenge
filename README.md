# Mercado Libre Challenge

## Stack
 1. Django 4.2.11
 2. Python 3.9.6

## GETTING STARTED

### With Docker
```
docker-compose up
```

### OR...

### Create virtualenv
```
python3 -m venv venv
```

### Install requirements
```
pip install -r requirements.txt
```

### Create .env file
An envirnoment  variables file can be found in the project: *.env.example*. This file shows env variables for settings in order to run project. For that purpose it was used [python-decouple](https://github.com/henriquebastos/python-decouple) package.
Rename this file with *.env* and then fill variables with your own.

### Database
For testing purposes, sqlite is currently selected, but it is possible to create the database with postgres or mysql.

Once you have defined all settings in _.env_ file, then you have to run django migrations.

```
python manage.py migrate
```

### Users
In order to start testing the project, it's necesary to have initial users and groups (for roles). For testing purposes, the project have a initial users and groups file (fixture) to load in the database.

To load users and groups data from fixtures:
```
python manage.py loaddata core/users_groups_fixture.json
```

These steps will load users and groups (user roles).

Password for all users is *melitest*.

 - manager1 (manager)
 - manager2 (manager)
 - manager3 (manager)
 - employee1 (employee)
 - employee2 (employee)
 - employee3 (employee)
 - customer1 (customer)
 - customer2 (customer)
 - customer3 (customer)

Additionally, a user with the superadmin role has been added. This user has all permissions granted, including access to the Django admin. The user is as follows:

- Username: admin
- Password: admin (for testing purposes)

### Run project
Once you have finished previous steps you can run project on local environment.
```
python manage.py runserver

```

### URLs (and permissions)
Below are the URLs and the roles that have access to those views:

The roles (manager) have permissions to see:
- http://localhost:8000/alta_empleado/
- http://localhost:8000/alta_cliente/
- http://localhost:8000/venta/reportes/

The roles (manager, employee) have permissions to see:
- http://localhost:8000/login/
- http://localhost:8000/alta_cliente/
- http://localhost:8000/inventario/
- http://localhost:8000/inventario/crear/
- http://localhost:8000/inventario/editar/[slug]/
- http://localhost:8000/venta/crear/
- http://localhost:8000/venta/lista/
- http://localhost:8000/venta/[uuid]/


The roles (manager, employee, customer) have permissions to see:
- http://localhost:8000/login
- http://localhost:8000/logout
- http://localhost:8000/venta/lista/

The role superadmin (user "admin"), have permissions to see:
- http://localhost:8000/django-admin/
