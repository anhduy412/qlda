import datetime
import sys
from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    sessions,
    url_for,
    send_file,
    abort,
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkeyhere'

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login1')
def login1():
    return render_template('login-1.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register')
def register1():
    return render_template('register-1.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/icons')
def icons():
    return render_template('icons.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    if 'local' in sys.argv:
        app.run(host="127.0.0.1", port=7777, debug=True)
    else:
        app.run(host="0.0.0.0", port=7777)