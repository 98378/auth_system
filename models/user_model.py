from db import get_db_connection
from mysql.connector import Error

class UserModel:
    
    @staticmethod
    def create(name, email, hashed_password, role, twofa_secret=None):
        connection = get_db_connection()
        if not connection:
            return None
        
        cursor = connection.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (name, email, password, role, twofa_secret) VALUES (%s, %s, %s, %s, %s)',
                (name, email, hashed_password, role, twofa_secret)
            )
            connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error creating user: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_by_email(email):
        connection = get_db_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            user = cursor.fetchone()
            return user
        except Error as e:
            print(f"Error finding user: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def find_by_id(user_id):
        connection = get_db_connection()
        if not connection:
            return None
        
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute('SELECT id, name, email, role FROM users WHERE id = %s', (user_id,))
            user = cursor.fetchone()
            return user
        except Error as e:
            print(f"Error finding user by id: {e}")
            return None
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def update_2fa_secret(email, secret):
        connection = get_db_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        try:
            cursor.execute('UPDATE users SET twofa_secret = %s WHERE email = %s', (secret, email))
            connection.commit()
            return True
        except Error as e:
            print(f"Error updating 2FA secret: {e}")
            return False
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_all_users():
        connection = get_db_connection()
        if not connection:
            return []
        
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute('SELECT id, name, email, role FROM users')
            users = cursor.fetchall()
            return users
        except Error as e:
            print(f"Error getting users: {e}")
            return []
        finally:
            cursor.close()
            connection.close()