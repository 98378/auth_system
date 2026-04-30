from flask import Flask, render_template
from flask_cors import CORS
from db import init_db
from routes.auth_routes import auth_bp
from routes.protected_routes import protected_bp

app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = app.config['SECRET_KEY']
CORS(app)

init_db()

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(protected_bp, url_prefix='/api')

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/register-page')
def register_page():
    return render_template('register.html')

@app.route('/verify-page')
def verify_page():
    return render_template('verify_2fa.html')

@app.route('/dashboard-page')
def dashboard_page():
    return render_template('dashboard.html')

@app.route('/profile-page')
def profile_page():
    return render_template('profile.html')

@app.route('/admin-page')
def admin_page():
    return render_template('admin.html')

@app.route('/manager-page')
def manager_page():
    return render_template('manager.html')

@app.route('/user-page')
def user_page():
    return render_template('user.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)