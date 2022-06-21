import datetime
import sys
from colorama import reinit
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
import pymongo
from mongo_connect import mongo_create
from bson.objectid import ObjectId
import api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkeyhere'

mydb=mongo_create()

@app.errorhandler(403)
def page_not_found(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500

@app.before_request
def before_request():
    g.user = None
    if 'user_name' in session:
        if mydb.user.find_one({'username': session['user_name']}):
            g.user = mydb.user.find_one({'username': session['user_name']})
        elif mydb.supporters.find_one({'email': session['user_name']}):
            g.user = mydb.supporters.find_one({'email': session['user_name']})
        elif mydb.partners.find_one({'email': session['user_name']}):
            g.user = mydb.partners.find_one({'email': session['user_name']})
        elif mydb.clients.find_one({'email': session['user_name']}):
            g.user = mydb.clients.find_one({'email': session['user_name']})

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

# @app.route('/login1', methods=['GET', 'POST'])
# def login1():
#     return render_template('login-1.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

# @app.route('/register1', methods=['GET', 'POST'])
# def register1():
#     return render_template('register-1.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# @app.route('/icons', methods=['GET', 'POST'])
# def icons():
#     return render_template('icons.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')

@app.route('/profile/edit', methods=['GET', 'POST'])
def profile_edit():
    return render_template('profile.html')

@app.route('/project', methods=['GET', 'POST'])
def project():
    return render_template('project.html')

@app.route('/project/add', methods=['GET', 'POST'])
def project_add():
    if request.method ==  'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        team = request.POST.get('team')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date_real')
        progress = request.POST.get('progress')
        insert_data = {
            'name': name,
            'description': description,
            'team': team,
            'start_date': start_date,
            'end_date': end_date,
            'progress': progress,
            }
        mydb.project.insert_one(insert_data)
        return redirect(url_for('project'))
    return render_template('project_add.html')

@app.route('/project/edit/<id>', methods=['GET', 'POST'])
def project_edit():
    if request.method ==  'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        team = request.POST.get('team')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date_real')
        progress = request.POST.get('progress')
        insert_data = {
            '_id': ObjectId(request.POST.get('_id')),
            'name': name,
            'description': description,
            'team': team,
            'start_date': start_date,
            'end_date': end_date,
            'progress': progress,
            }
        mydb.project.update_one(insert_data)
        return redirect(url_for('project'))
    return render_template('project_edit.html')

@app.route('/project/delete/<id>', methods=['GET', 'POST'])
def project_delete():
    mydb.project.delete_one({'_id': ObjectId(_id)})
    return  render_template('project.html')

@app.route('/work')
def work():
    return render_template('work.html')

@app.route('/work/add/<id>', methods=['GET', 'POST'])
def work_create():
    if methods == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        team = request.POST.get('team')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date_real')
        progress = request.POST.get('progress')
        insert_data = {
            'name': name,
            'description': description,
            'team': team,
            'start_date': start_date,
            'end_date': end_date,
            'progress': progress,
            }
        mydb.work.update_one(insert_data)
        return redirect(url_for('project'))
    return render_template('work.html')

@app.route('/work/edit/<id>', methods=['GET', 'POST'])
def work_edit():
    if request.method ==  'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        team = request.POST.get('team')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date_real')
        progress = request.POST.get('progress')
        insert_data = {
            'name': name,
            'description': description,
            'team': team,
            'start_date': start_date,
            'end_date': end_date,
            'progress': progress,
            }
        mydb.work.insert_one(insert_data)
        return redirect(url_for('project'))
    return render_template('work.html')

@app.route('/work/delete/<id>', methods=['GET', 'POST'])
def work_delete():
    return render_template('work.html')

if __name__ == '__main__':
    if 'local' in sys.argv:
        app.run(host="127.0.0.1", port=7777, debug=True)
    else:
        app.run(host="0.0.0.0", port=7777)