from os import environ

POSTGRES = {
    'user': environ.get('POSTGRES_USER'),
    'pw': environ.get('POSTGRES_PASS'),
    'db': environ.get('POSTGRES_DB'),
    'host': environ.get('POSTGRES_HOST'),
    'port': environ.get('POSTGRES_PORT'),
}

SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_TRACK_MODIFICATIONS = False

REDIS_URI = "localhost"
REDIS_DB = "10"
DEBUG = True
