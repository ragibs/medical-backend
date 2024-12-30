import mysql.connector
from dotenv import dotenv_values
import os
from urllib.parse import urlparse


# Loading Enviornment Variables
env_path = os.path.join('..', 'Virtual', '.env')
secrets = dotenv_values(env_path)

dataBase = mysql.connector.connect(
    host = secrets['SQL_HOST'],
    port= secrets['SQL_PORT'],
    user = secrets['SQL_USERNAME'],
    passwd = secrets['SQL_PASSWORD']
)

# Prepare a cursor object
cursorObject = dataBase.cursor()

# create a database
cursorObject.execute("CREATE DATABASE medicalapp")

print("Database Created")