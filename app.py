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
import pymongo
from bson.objectid import ObjectId
from flask_paginate import Pagination
from mongo_connect import mongo_create
import api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkeyhere'
mydb=mongo_create()
ITEMS_PER_PAGE = 10

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
    if 'username' in session:
        if mydb.user.find_one({'username': session['username']}):
            g.user = mydb.user.find_one({'username': session['username']})

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        session.pop('username', None)
        username = request.form.get('username').strip()
        password = request.form.get('password').strip()
        if username == '':
            error = "Tên người dùng không được để trống"
            return render_template('login.html', error=error)
        if password == '':
            error = "Bạn vui lòng nhập mật khẩu đăng nhập"
            return render_template('login.html', error=error)
        current_user = mydb.user.find_one(
            {'$or': [{'username': username}]})
        if current_user:
            if (api.verify_password(password, current_user.get('password'))):
                session.permanent = True
                session['user_name'] = current_user.get('email')
                session['id'] = str(current_user.get('_id'))
                return redirect(url_for('start'))
            else:
                error = "Sai tài khoản hoặc mật khẩu"
                return render_template('login.html', error=error)
        else:
            error = "Sai tài khoản hoặc mật khẩu"
            return render_template('login.html', error=error)
        return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        email = request.form.get('email')
        position = request.form.get('position')
        team = request.form.get('team')
        insert_data = {
            'username': username,
            'password': password,
            'name': name,
            'gender': gender,
            'phone': phone,
            'email': email,
            'position': position,
            'team': team,
        }
        mydb.user.insert_one(insert_data)
        return redirect(url_for('login'))
    gender = [
        {
            'display_name': 'Nam',
            'value': 'male',
        },
        {
            'display_name': 'Nữ',
            'value': 'Female',
        },
    ]
    position = [
        {
            'display_name': 'Quản lý',
            'value': 'manager',
        },
        {
            'display_name': 'Trưởng ban',
            'value': 'leader',
        },
        {
            'display_name': 'Thành viên',
            'value': 'member',
        },
    ]
    team = [
        {
            'display_name': 'Lập trình',
            'value': 'dev',
        },
        {
            'display_name': 'Dữ liệu',
            'value': 'data',
        },
        {
            'display_name': 'Kinh doanh',
            'value': 'sale',
        },
    ]
    return render_template('register.html', gender=gender, position=position, team=team)

@app.route('/', methods=['GET', 'POST'])
def index():
    # if not g.user:
    #     return redirect(url_for('login'))
    return render_template('index.html')

# @app.route('/profile/<id>', methods=['GET', 'POST'])
# def profile(user_id):
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    # if not g.user:
    #     return redirect(url_for('login'))
    if request.method == 'POST':
        password = request.form.get('password')
        gender = request.form.get('gender')
        email = request.form.get('email')
        phone = request.form.get('phone')
        position = request.form.get('position')
        team = request.form.get('team')
        new_data = {
            'password': password,
            'gender': gender,
            'email': email,
            'phone': phone,
            'position': position,
            'team': team,
        }
        mydb.user.update_one({"_id": ObjectId()}, {"$set": new_data},)
    gender = [
        {
            'display_name': 'Nam',
            'value': 'male',
        },
        {
            'display_name': 'Nữ',
            'value': 'Female',
        },
    ]
    position = [
        {
            'display_name': 'Quản lý',
            'value': 'manager',
        },
        {
            'display_name': 'Trưởng ban',
            'value': 'leader',
        },
        {
            'display_name': 'Thành viên',
            'value': 'member',
        },
    ]
    team = [
        {
            'display_name': 'Lập trình',
            'value': 'dev',
        },
        {
            'display_name': 'Dữ liệu',
            'value': 'data',
        },
        {
            'display_name': 'Kinh doanh',
            'value': 'sale',
        },
    ]
    return render_template('profile.html', gender=gender, position=position, team=team)

@app.route('/project', methods=['GET', 'POST'])
def project():
    # if not g.user:
    #     return redirect(url_for('login'))
    filter = {

    }
    name = request.args.get('name')
    description = request.args.get('description')
    team = request.args.get('team')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    status = request.args.get('status')
    selected_value = {
        'name': name,
        'description': description,
        'team': team,
        'start_date': start_date,
        'end_date': end_date,
        'status': status
    }
    cid_list = api.project.distinct('cid', {})
    count_logs = api.project.count_documents(filter)
    page = int(request.args.get('page', 1))
    pagination = Pagination(
        page=page,
        total=count_logs,
        per_page=ITEMS_PER_PAGE,
        css_framework='bootstrap3')
    recs = api.project.find(filter).sort("created_at", pymongo.DESCENDING).skip(
        ITEMS_PER_PAGE * (page - 1)).limit(ITEMS_PER_PAGE)
    return render_template('project.html', project_list=recs, pagination=pagination, selected_value=selected_value, count_logs=count_logs, cid_list=cid_list)

@app.route('/project/add', methods=['GET', 'POST'])
def project_add():
    # if not g.user:
    #     return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        team = request.form.get('team')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        insert_data = {
            'name': name,
            'description': description,
            'team': team,
            'start_date': start_date,
            'end_date': end_date,
            }
        mydb.project.insert_one(insert_data)
        return redirect(url_for('project'))
    project_list = api.project.find()
    team = [
        {
            'display_name': 'Lập trình',
            'value': 'dev',
        },
        {
            'display_name': 'Dữ liệu',
            'value': 'data',
        },
        {
            'display_name': 'Kinh doanh',
            'value': 'sale',
        },
    ]
    return render_template('project-add.html', project_list=project_list, team=team)

@app.route('/project/edit/<id>', methods=['GET', 'POST'])
def project_edit(project_id):
    # if not g.user:
    #     return redirect(url_for('login'))
    if request.method ==  'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        team = request.form.get('team')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date_real')
        progress = request.form.get('progress')
        new_data = {
            'name': name,
            'description': description,
            'team': team,
            'start_date': start_date,
            'end_date': end_date,
            'progress': progress,
            }
        mydb.project.update_one(new_data)
        return redirect(url_for('project'))
    return render_template('project_edit.html')

@app.route('/project/delete/<id>', methods=['GET', 'POST'])
def project_delete(project_id):
    # if not g.user:
    #     return redirect(url_for('login'))
    # mydb.project.delete_one({'_id': ObjectId(_id)})
    mydb.project.delete_one({'_id': ObjectId(project_id)})
    return  render_template('project.html')

@app.route('/work')
def work():
    # if not g.user:
    #     return redirect(url_for('login'))
    filter = {

    }
    name = request.args.get('name')
    description = request.args.get('description')
    team = request.args.get('team')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    status = request.args.get('status')
    selected_value = {
        'name': name,
        'description': description,
        'team': team,
        'start_date': start_date,
        'end_date': end_date,
        'status': status
    }
    cid_list = api.work.distinct('cid', {})
    count_logs = api.work.count_documents(filter)
    page = int(request.args.get('page', 1))
    pagination = Pagination(
        page=page,
        total=count_logs,
        per_page=ITEMS_PER_PAGE,
        css_framework='bootstrap3')
    recs = api.work.find(filter).sort("created_at", pymongo.DESCENDING).skip(
        ITEMS_PER_PAGE * (page - 1)).limit(ITEMS_PER_PAGE)
    return render_template('work.html', work_list=recs, pagination=pagination, selected_value=selected_value, count_logs=count_logs, cid_list=cid_list)

    return render_template('work.html')

@app.route('/work/add', methods=['GET', 'POST'])
def work_create():
    # if not g.user:
    #     return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form.get('name')
        project_name = request.form.get('project_name')
        description = request.form.get('description')
        team = request.form.get('team')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        insert_data = {
            'name': name,
            'description': description,
            'team': team,
            'start_date': start_date,
            'end_date': end_date,
        }
        mydb.work.insert_one(insert_data)
        return redirect(url_for('work'))
    work_list = api.work.find()
    team = [
        {
            'display_name': 'Lập trình',
            'value': 'dev',
        },
        {
            'display_name': 'Dữ liệu',
            'value': 'data',
        },
        {
            'display_name': 'Kinh doanh',
            'value': 'sale',
        },
    ]
    return render_template('work-add.html', work_list=work_list, team=team)

@app.route('/work/edit/<id>', methods=['GET', 'POST'])
def work_edit():
    # if not g.user:
    #     return redirect(url_for('login'))
    if request.method ==  'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        team = request.form.get('team')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date_real')
        progress = request.form.get('progress')
        new_data = {
            'name': name,
            'description': description,
            'team': team,
            'start_date': start_date,
            'end_date': end_date,
            'progress': progress,
        }
        mydb.work.insert_one(new_data)
        return redirect(url_for('work'))
    return render_template('work-edit.html')

@app.route('/work/delete/<id>', methods=['GET', 'POST'])
def work_delete():
    # if not g.user:
    #     return redirect(url_for('login'))
    return render_template('work.html')

@app.route('/table', methods=['GET', 'POST'])
def table():
    # if not g.user:
    #     return redirect(url_for('login'))
    return render_template('table.html')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    if 'local' in sys.argv:
        app.run(host="127.0.0.1", port=7777, debug=True)
    else:
        app.run(host="0.0.0.0", port=7777)