

# Social Team Builder (Djenga Circle v2)

A Treehouse Python Web Development Techdegree Capstone Project

## Setting Up
- After downloading files, create a virtualenv in the project folder.  
`python -m venv env`  
- Activate virtualenv.  
`env\scripts\activate`  
- Use pip to install requirements.  
`pip install -r requirements.txt`  
- From the primary backend folder, make migrations.  
`python manage.py makemigrations`
- Apply migrations.  
`python manage.py migrate`

## Creating a Superuser
- Create a superuser with username, email and password.  
`python manage.py createsuperuser`
