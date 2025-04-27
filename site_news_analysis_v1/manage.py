#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website_configs.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

#django-admin startproject website_configs(建立django專案)
#python manage.py runserver 8000(執行伺服器)
#python manage.py startapp app_key_person (django-admin startapp app_taiwan_mayor)

#讓命令列可以與conda虛擬環境整合。
#$>conda init powershell

#Create a virtual environment
#conda create -n name python=3.11(版本)

#看看有那些虛擬環境
#conda env list

#進入和離開虛擬環境
#activate my_env(name)
#conda activate my_env(name)
#deactivate
