import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET = os.environ.get('JWT_SECRET')
    
    # MySQL Workbench Configuration
    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''  # <- change this to your MySQL password
    MYSQL_DATABASE = 'auth_system'