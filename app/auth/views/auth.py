import functools
from flask import flash, render_template, Blueprint, redirect, url_for, request
from flask import session, g
from ..models import auth
from werkzeug.security import check_password_hash, generate_password_hash
from RealProject import db
from app.forms import LoginForm, RegisterForm

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

def login_required(view):
    # 装饰器函数，检查用户是否登录
    #限制必须登录才能访问的页面装饰器
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            redirect_to = f"{url_for('auth.login')}?redirect={request.path}"
            return redirect(redirect_to)
        # 如果用户已经登录，则继续执行视图函数
        return view(**kwargs)
    return wrapped_view


@bp.route('/login', methods=['GET', 'POST'])
def login():

    redirect_to = request.args.get('redirect_to') 
    form = LoginForm()
    #form = loginform(metadata={'csrf_context': csrf_context})
    #禁用csrf
    if form.validate_on_submit():
        user = auth.User.query.filter_by(username=form.username.data).first()
        session.clear()  # 清除之前的session
        session['user_id'] = user.id
        if redirect_to is not None:
            return redirect(redirect_to)  # 登录成功跳转到之前的页面

        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
     # 注册视图
    form = RegisterForm()
    if form.validate_on_submit():
        user = auth.User(username=form.username.data, password=generate_password_hash(form.password.data))
        db.session.add(user)
        db.session.commit()
        session.clear()
        session['user_id'] = user.id
        return redirect(url_for('index'))  # 注册成功跳转到主页       
    return render_template('register.html', form=form)

@bp.route('/logout')
def logout():
    session.clear()  # 清除session注销
    return redirect(url_for('index'))


