from dotenv import load_dotenv
import os
load_dotenv()

env = os.getenv('ENVIRONMENT')

if env == 'development':
    host = os.getenv('DEV_DB_HOST')
    port = os.getenv('DEV_DB_PORT')
    user = os.getenv('DEV_DB_USER')
    password = os.getenv('DEV_DB_PASSWORD')
    db_name = os.getenv('DEV_DB_NAME')

if env == 'testing':
    host = os.getenv('TEST_DB_HOST')
    port = os.getenv('TEST_DB_PORT')
    user = os.getenv('TEST_DB_USER')
    password = os.getenv('TEST_DB_PASSWORD')
    db_name = os.getenv('TEST_DB_NAME')

if env == 'production':
    host = os.getenv('PROD_DB_HOST')
    port = os.getenv('PROD_DB_PORT')
    user = os.getenv('PROD_DB_USER')
    password = os.getenv('PROD_DB_PASSWORD')
    db_name = os.getenv('PROD_DB_NAME')

server_host = os.getenv('SERVER_HOST')
server_port = int(os.getenv('SERVER_PORT'))

db_url = os.getenv('DB_URL')

