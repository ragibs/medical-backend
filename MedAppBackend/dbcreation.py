# Install Mysql on your computer
# https://dev.mysql.com/downloads/installer/
# pip install mysql
# pip install mysql-connector
# pip install mysql-connector-python 

import mysql.connector
from dotenv import dotenv_values
import os

# Loading Enviornment Variables
env_path = os.path.join('..', 'Virtual', '.env')
secrets = dotenv_values(env_path)

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = secrets['SQL_USERNAME'],
    passwd = secrets['SQL_PASSWORD']
)

# Prepare a cursor object
cursorObject = dataBase.cursor()

# create a database
cursorObject.execute("CREATE DATABASE medicalapp")

print("Database Created")