from decouple import config

DEBUG = config("DEBUG", default = False, cast=bool)
SECRET_KEY = config("SECRET_KEY")
