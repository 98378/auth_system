import bcrypt
import jwt
import pyotp
import qrcode
from io import BytesIO
import base64
from datetime import datetime, timedelta
from config import Config

# Password Hashing
def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# JWT Token
def generate_token(user_id, email, role):
    payload = {
        'user_id': user_id,
        'email': email,
        'role': role,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, Config.JWT_SECRET, algorithm='HS256')

def verify_token(token):
    try:
        return jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
    except:
        return None

# 2FA with pyotp
def generate_2fa_secret():
    return pyotp.random_base32()

def get_qr_code(secret, email):
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=email, issuer_name='AuthSystem')
    
    qr = qrcode.make(uri)
    buffered = BytesIO()
    qr.save(buffered, format="PNG")
    qr_base64 = base64.b64encode(buffered.getvalue()).decode()
    
    return qr_base64, secret

def verify_2fa_code(secret, user_code):
    totp = pyotp.TOTP(secret)
    return totp.verify(user_code)

# Password Strength Validation
def check_password_strength(password):
    errors = []
    
    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")
    
    if not any(char.isupper() for char in password):
        errors.append("Password must contain at least one uppercase letter")
    
    if not any(char.islower() for char in password):
        errors.append("Password must contain at least one lowercase letter")
    
    if not any(char.isdigit() for char in password):
        errors.append("Password must contain at least one number")
    
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if not any(char in special_chars for char in password):
        errors.append("Password must contain at least one special character (!@#$%^&* etc.)")
    
    return len(errors) == 0, errors