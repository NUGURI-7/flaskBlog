from flask import flash, render_template, Blueprint, redirect, url_for, request
from flask import session, g
from ..models import auth
from werkzeug.security import check_password_hash, generate_password_hash
from RealProject import db

bp = Blueprint('auth', __name__, url_prefix='/auth', 
               template_folder='../templates', 
               static_folder='../static')


#注册一个在视图函数之前运行的函数
@bp.before_app_request
def load_logged_in_user():
    # 在每个请求之前都回去session中查看userID来获取用户
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = auth.User.query.get(user_id)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        user = auth.User.query.filter_by(username=username).first()
        if user is None:
            error = '用户名不存在'
        elif not check_password_hash(user.password, password):
            #验证数据库中密文和表单提交的密码是否一致   
            error = '密码错误'        

        if error is None:
            # 登录成功后设置session
            session.clear()  # 清除之前的session
            session['user_id'] = user.id
            return redirect(url_for('index'))
        # 登录成功跳转到主页
        flash(error)
    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password1 = request.form['password1']
        
        if password != password1:
            flash('两次输入的密码不一致')
        
        exist_user = auth.User.query.filter_by(username=username).first()
        if exist_user:
            flash('用户名已存在,请更换其他用户名!')
            # return redirect(url_for('auth.register'))       
        else:
            user = auth.User(username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()

            #注册成功自动登录
            session.clear()   # 清除之前的session
            # 注册成功后设置session
            session['user_id'] = user.id
        return redirect(url_for('index'))  # 注册成功跳转到主页       
    return render_template('register.html')

@bp.route('/logout')
def logout():
    session.clear()  # 清除session注销
    return redirect(url_for('index'))


