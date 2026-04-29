import os

class Config:
    SECRET_KEY = 'your-super-secret-key-change-in-production-2024'
    JWT_SECRET = 'jwt-secret-key-change-this-2024'
    
    # MySQL Workbench Configuration
    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''  # <- change this to your MySQL password
    MYSQL_DATABASE = 'auth_system'