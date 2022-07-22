# KanalServis

### Installation
1. clone repository `git@github.com:jetigenov/kanal.git`
2. create virtualenv with python3.7 `virtualenv venv`
3. install postgres 13 `brew install postgresql@13`
4. install requirements `pip install -r requirements.txt`
5. make migrations
    - `python db_manage.py db init`
    - `python db_manage.py db migrate`
    - `python db_manage.py db upgrade`
6. runserver
    - `python db_manage.py runserver`

### Build Docker main image
1. run `build.sh` to build docker image
2. copy `docker-compose-example.yml` or add services to your `docker-compose.yml`
3. copy `example.env` to `.env` or copy variables to your env file
4. run docker-compose `docker-compose up -d`
5. run psql in postgres container: `docker-compose exec postgres psql -U posgtres`
6. create database: `postgres=# CREATE DATABASE kanal;`

##### Read sheet from another account via api_key
`this method need for gets data from google sheets and get currency by date from bank api after manipulatig save data to database` 
- URL: `/manager/import.get_sheet`
- POST_METHOD: `POST` BODY - `{ }`

##### Write sheet from database via api_key
`this method need for save data from database to google sheets` 
- URL: `/manager/import.update_sheet`
- POST_METHOD: `POST` BODY - `{ }`