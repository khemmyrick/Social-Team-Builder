import json
from os import environ
from os import path
import sys

import django


BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

PROJ_DIR = path.dirname(BASE_DIR)

sys.path.insert(0, PROJ_DIR)

def load_data():
    # Load User Serializer.
    try:
        from accounts.serializers import UserSerializer
    except ImportError:
        raise ImportError(
            'serializers.py must contain a properly '
            'implemented UserSerializer class for this import to work.'
        )

    filepath = path.join(PROJ_DIR, 'assets', 'user_details.json')
    
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
        itera = 1
        for item in data:
            print(str(itera) + ': ' + item['display_name'])
            itera += 1

        serializer = UserSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            print('Users loaded.')
        else:
            print(serializer.errors)
            print('load_data unsuccessful.')

    # Load Skill Serializer.
    try:
        from accounts.serializers import SkillSerializer
    except ImportError:
        raise ImportError(
            'serializers.py must contain a properly '
            'implemented SkillSerializer class for this import to work.'
        )

    filepath = path.join(PROJ_DIR, 'assets', 'skills.json')
    
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
        itera = 1
        for item in data:
            print(str(itera) + ': ' + item['name'])
            itera += 1

        serializer = SkillSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            print('Skills loaded.')
        else:
            print(serializer.errors)
            print('load_data unsuccessful.')

    # Load Project Serializer.
    try:
        from projects.serializers import ProjectSerializer
    except ImportError:
        raise ImportError(
            'serializers.py must contain a properly '
            'implemented ProjectSerializer class for this import to work.'
        )

    filepath = path.join(PROJ_DIR, 'assets', 'project_details.json')
    
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
        itera = 1
        for item in data:
            print(str(itera) + ': ' + item['name'])
            itera += 1

        serializer = ProjectSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            print('Projects loaded.')
        else:
            print(serializer.errors)
            print('load_data unsuccessful.')

    # Load Position Serializer.
    try:
        from projects.serializers import PositionSerializer
    except ImportError:
        raise ImportError(
            'serializers.py must contain a properly '
            'implemented PositionSerializer class for this import to work.'
        )

    filepath = path.join(PROJ_DIR, 'assets', 'position_details.json')
    
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
        itera = 1
        for item in data:
            print(str(itera) + ': ' + item['name'])
            itera += 1

        serializer = ProjectSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            print('Positions loaded.')
        else:
            print(serializer.errors)
            print('load_data unsuccessful.')


    # Load Applicant Serializer.
    try:
        from projects.serializers import ApplicantSerializer
    except ImportError:
        raise ImportError(
            'serializers.py must contain a properly '
            'implemented ApplicantSerializer class for this import to work.'
        )

    filepath = path.join(PROJ_DIR, 'assets', 'applicant_details.json')
    
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
        itera = 1
        for item in data:
            print(str(itera) + ': ' + item['name'])
            itera += 1

        serializer = ApplicantSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            print('Applicants loaded.')
        else:
            print(serializer.errors)
            print('load_data unsuccessful.')


if __name__ == '__main__':
    # sys.path.append(PROJ_DIR) ##### MIGHT HAVE TO KEEP THIS FOR DJANGO 2+
    environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    django.setup()
    load_data()