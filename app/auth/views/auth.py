from flask import render_template, Blueprint, redirect, url_for, request
from ..models import auth

bp = Blueprint('auth', __name__, url_prefix='/auth', 
               template_folder='../templates', 
               static_folder='../static')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 登录相关逻辑代码
        pass  # Placeholder to fix indentation error

    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 注册相关逻辑代码

        # 注册成功跳转到登录页
        return redirect(url_for('auth.login'))

    return render_template('register.html')