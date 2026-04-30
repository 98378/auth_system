from flask import Blueprint, request, jsonify, session
from models.user_model import UserModel
from utils.auth_utils import (
    hash_password, verify_password,
    generate_2fa_secret, get_qr_code, verify_2fa_code,
    generate_token, check_password_strength
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    
    # Validation All fields required
    if not all([name, email, password, role]):
        return jsonify({'error': 'All fields (name, email, password, role) are required'}), 400
    
    # Role validation
    if role not in ['admin', 'manager', 'user']:
        return jsonify({'error': 'Role must be admin, manager, or user'}), 400
    
    # Check if email already exists
    if UserModel.find_by_email(email):
        return jsonify({'error': 'Email already exists'}), 409
    
    # Password Strength Check
    is_strong, password_errors = check_password_strength(password)
    if not is_strong:
        return jsonify({
            'error': 'Password is too weak',
            'requirements': password_errors
        }), 400
    
    # Hash password
    hashed_password = hash_password(password)
    
    # Generate 2FA secret (returns string directly)
    twofa_secret = generate_2fa_secret()
    
    # Save user to database
    UserModel.create(name, email, hashed_password, role, twofa_secret)
    
    # Generate QR code for 2FA
    qr_base64, _ = get_qr_code(twofa_secret, email)
    
    return jsonify({
        'message': 'User registered successfully',
        'qr_code': qr_base64,
        'secret': twofa_secret,
        'instruction': 'Scan this QR code with Google Authenticator'
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    user = UserModel.find_by_email(email)
    
    if not user or not verify_password(password, user['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    session['temp_user_email'] = email
    return jsonify({'message': 'Password verified. Enter 2FA code.', 'requires_2fa': True}), 200


@auth_bp.route('/verify-2fa', methods=['POST'])
def verify_2fa():
    data = request.get_json()
    code = data.get('code')
    email = session.get('temp_user_email')
    
    if not email:
        return jsonify({'error': 'Session expired. Login again.'}), 401
    
    user = UserModel.find_by_email(email)
    
    if not user or not verify_2fa_code(user['twofa_secret'], code):
        return jsonify({'error': 'Invalid 2FA code'}), 401
    
    token = generate_token(user['id'], user['email'], user['role'])
    session.pop('temp_user_email', None)
    
    return jsonify({
        'message': 'Authentication successful',
        'token': token,
        'user': {
            'id': user['id'],
            'name': user['name'],
            'email': user['email'],
            'role': user['role']
        }
    }), 200


@auth_bp.route('/get-qr-code', methods=['POST'])
def get_qr_code_again():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    user = UserModel.find_by_email(email)
    
    if not user or not verify_password(password, user['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if not user['twofa_secret']:
        return jsonify({'error': 'No 2FA secret found for this user'}), 404
    
    qr_base64, secret = get_qr_code(user['twofa_secret'], email)
    
    return jsonify({
        'qr_code': qr_base64,
        'secret': secret,
        'message': 'Scan this QR code with Google Authenticator'
    }), 200