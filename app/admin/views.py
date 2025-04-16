from flask import (Blueprint, render_template, request, redirect,
                    url_for, flash, session)

from app.auth.views.auth import login_required
from app.blog.models import Category
from app.admin.forms import CategoryCreateForm
from RealProject import db



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
        -Category.add_date).paginate(page=page, per_page=2, error_out=False)
    category_list = pagination.items
    return render_template(
        'admin/category.html', 
        category_list=category_list, 
        pagination=pagination
    )


#新增分类视图
@bp.route('/category/add', methods=['GET', 'POST'])
@login_required
def category_add():
    # 增加分类
    form = CategoryCreateForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, icon=form.icon.data)
        db.session.add(category)
        db.session.commit()
        flash(f'{form.name.data}分类添加成功')
        return redirect(url_for('admin.category'))
    return render_template('admin/category_form.html', form=form)

#编辑分类视图
@bp.route('/category/edit/<int:cate_id>', methods=['GET', 'POST'])
@login_required
def category_edit(cate_id):
    # 增加分类
    category = Category.query.get(cate_id)
    form = CategoryCreateForm(name=category.name, icon=category.icon)
    if form.validate_on_submit():
        category.name = form.name.data
        category.icon = form.icon.data
        db.session.add(category)
        db.session.commit()
        flash(f'{form.name.data}分类修改成功')
        return redirect(url_for('admin.category'))
    return render_template('admin/category_form.html', form=form)

# 删除分类视图
@bp.route('/category/delete/<int:cate_id>')
@login_required
def category_del(cate_id):
    cate = Category.query.get(cate_id)
    if cate:
        # 级联删除
        # Post.query.filter(Post.category_id==cate.id).delete()
        db.session.delete(cate)
        db.session.commit()
        flash(f'{cate.name}分类删除成功')
        return redirect(url_for('admin.category'))