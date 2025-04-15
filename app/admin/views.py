from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.auth.views.auth import login_required

bp = Blueprint('admin',__name__, url_prefix='/admin',
               static_folder='static', template_folder='templates')


#创建后台管理的首页
@bp.route('/')
@login_required
def index():
   
    return render_template('admin/index.html')
