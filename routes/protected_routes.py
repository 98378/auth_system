from flask import Blueprint, request, jsonify
from functools import wraps
from utils.auth_utils import verify_token

protected_bp = Blueprint('protected', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = verify_token(token)
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        request.user = payload
        return f(*args, **kwargs)
    return decorated
def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user_role = request.user.get('role')
            if user_role not in allowed_roles:
                return jsonify({
                    'error': 'Access Denied',
                    'message': f'❌ This page is only for: {", ".join(allowed_roles)}',
                    'your_role': user_role
                }), 403
            return f(*args, **kwargs)
        return decorated
    return decorator
# ========== Admin Panel - Only Admin ==========
@protected_bp.route('/admin', methods=['GET'])
@token_required
@role_required(['admin'])
def admin_panel():
    return jsonify({
        'message': 'Welcome to Admin Panel',
        'user': request.user,
        'permissions': ['manage_users', 'view_all', 'delete_users', 'system_settings']
    }), 200


# ========== Manager Panel - Only Manager (NOT Admin) ==========
@protected_bp.route('/manager', methods=['GET'])
@token_required
@role_required(['manager'])
def manager_panel():
    return jsonify({
        'message': 'Welcome to Manager Panel',
        'user': request.user,
        'permissions': ['view_team', 'manage_reports', 'approve_requests']
    }), 200


# ========== User Panel - Only User (NOT Admin or Manager) ==========
@protected_bp.route('/user', methods=['GET'])
@token_required
@role_required(['user'])
def user_panel():
    return jsonify({
        'message': 'Welcome to User Panel',
        'user': request.user,
        'permissions': ['view_profile', 'edit_settings', 'view_dashboard']
    }), 200


# ========== Profile - Everyone ==========
@protected_bp.route('/profile', methods=['GET'])
@token_required
def profile():
    return jsonify({
        'message': 'Your Profile',
        'user': request.user
    }), 200


# ========== Dashboard - Everyone ==========
@protected_bp.route('/dashboard', methods=['GET'])
@token_required
def dashboard():
    return jsonify({
        'message': f'Welcome to Dashboard, {request.user["email"]}!',
        'user': request.user
    }), 200