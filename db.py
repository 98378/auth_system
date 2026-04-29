import mysql.connector
from mysql.connector import Error
from config import Config

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE
        )
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def get_db():
    return get_db_connection()

def init_db():
    connection = get_db_connection()
    if not connection:
        print("Failed to connect to database.")
        return
    
    cursor = connection.cursor()
    
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.MYSQL_DATABASE}")
    cursor.execute(f"USE {Config.MYSQL_DATABASE}")
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            role ENUM('admin', 'manager', 'user') NOT NULL,
            twofa_secret VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    connection.commit()
    cursor.close()
    connection.close()
    print("Database initialized successfully!")