"""Class-based Flask app configuration."""
from os import environ, path

basedir = path.abspath(path.dirname(__file__))


class Config:
    CSRF_ENABLED = True
    SECRET_KEY = 'you-will-never-guess'
    UPLOAD_FOLDER = '/home/ivanetc/PycharmProjects/genre_server/temp_files_storage'
