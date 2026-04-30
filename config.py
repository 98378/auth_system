import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'super-secret-key-2024-for-flask-session')
    JWT_SECRET = os.environ.get('JWT_SECRET', 'jwt-secret-key-for-token-2024')
    
    # MySQL Workbench Configuration
    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''  
    MYSQL_DATABASE = 'auth_system'