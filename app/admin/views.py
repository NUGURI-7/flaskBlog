from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from app.auth.views.auth import login_required
from app.blog.models import Category




bp = Blueprint('admin',__name__, url_prefix='/admin',
               static_folder='static', template_folder='templates')


#创建后台管理的首页
@bp.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@bp.route('/category')
@login_required
def category():
    # 查看分类
    page = request.args.get('page', 1, type=int)
    pagination = Category.query.order_by(
        -Category.add_date).paginate(page=page, per_page=10, error_out=False)
    category_list = pagination.items
    return render_template(
        'admin/category.html', 
        category_list=category_list, 
        pagination=pagination
    )