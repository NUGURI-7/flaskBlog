from flask import (Blueprint, render_template, request, redirect,
                    url_for, flash, session)

from app.auth.views.auth import login_required
from app.blog.models import Category, Post, Tag
from app.admin.forms import CategoryCreateForm, PostForm, TagForm
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
        Post.query.filter(Post.category_id==cate.id).delete()
        db.session.delete(cate)
        db.session.commit()
        flash(f'{cate.name}分类删除成功')
        return redirect(url_for('admin.category'))
    

#查看文章列表视图
@bp.route('/article')
@login_required
def article():
    # 查看文章列表
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(-Post.add_date).paginate(
        page=page, per_page=2, error_out=False)
    post_list = pagination.items
    return render_template('admin/article.html', 
                           post_list=post_list, pagination=pagination)    


#添加文章视图
@bp.route('/article/add', methods=['GET', 'POST'])
@login_required
def article_add():
    # 新增博客分类
    form = PostForm()
    form.category_id.choices = [(v.id,v.name) for v in Category.query.all()]
    form.tags.choices = [(v.id,v.name) for v in Tag.query.all()]

    if form.validate_on_submit():
        post = Post(
            title=form.title.data, 
            desc=form.desc.data, 
            has_type=form.has_type.data, 
            category_id=int(form.category_id.data),  #一对多保存
            content=form.content.data,
        )
        post.tags = [Tag.query.get(tag_id) for tag_id in form.tags.data] #多对多保存
        db.session.add(post)
        db.session.commit()
        flash(f'{form.title.data}文章添加成功')
        return redirect(url_for('admin.article'))
    return render_template('admin/article_form.html', form=form)


#编辑文章视图
@bp.route('/article/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def article_edit(post_id):
    # 回显数据
    post = Post.query.get(post_id)
    tags = [tag.id for tag in post.tags]  # 获取当前文章的标签ID
    form = PostForm(
        title=post.title, 
        desc=post.desc, 
        has_type=post.has_type.value, 
        category_id=post.category_id, 
        content=post.content,
        tags=tags,  
    )
    form.category_id.choices = [(v.id,v.name) for v in Category.query.all()]
    form.tags.choices = [(v.id,v.name) for v in Tag.query.all()]
    #修改数据
    if form.validate_on_submit():
        post.title = form.title.data
        post.desc = form.desc.data
        post.has_type = form.has_type.data
        post.category_id=int(form.category_id.data)
        post.content = form.content.data
        post.tags = [Tag.query.get(tag_id) for tag_id in form.tags.data]
        db.session.add(post)
        db.session.commit()
        flash(f'{form.title.data}文章修改成功')
        return redirect(url_for('admin.article'))
    return render_template('admin/article_form.html', form=form)

# 删除文章视图
@bp.route('/article/delete/<int:post_id>', methods=['GET', 'POST'])
@login_required
def article_del(post_id):
    post = Post.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        flash(f'{post.title}文章删除成功')
        return redirect(url_for('admin.article'))
    

# 标签列表视图
@bp.route('/tag')
@login_required
def tag():
    # 查看标签列表
    page = request.args.get('page', 1, type=int)
    pagination = Tag.query.order_by(-Tag.add_date).paginate(
        page=page, per_page=2, error_out=False)
    return render_template('admin/tag.html',
                           tag_list=pagination.items, 
                           pagination=pagination)
 
# 添加标签视图
@bp.route('/tag/add', methods=['GET', 'POST'])
@login_required
def tag_add():
    # 新增标签
    form = TagForm()
    if form.validate_on_submit():
        tag = Tag(name=form.name.data)
        db.session.add(tag)
        db.session.commit()
        flash(f'{form.name.data}添加成功')
        return redirect(url_for('admin.tag'))
    return render_template('admin/tag_form.html', form=form)

# 编辑标签视图
@bp.route('/tag/edit/<int:tag_id>', methods=['GET', 'POST'])
@login_required
def tag_edit(tag_id):
    # 编辑标签
    tag = Tag.query.get(tag_id)
    form = TagForm(name=tag.name)
    if form.validate_on_submit():
        tag.name = form.name.data
        db.session.add(tag)
        db.session.commit()
        flash(f'{form.name.data}修改成功')
        return redirect(url_for('admin.tag'))
    return render_template('admin/tag_form.html', form=form)

# 删除标签视图
@bp.route('/tag/delete/<int:tag_id>', methods=['GET', 'POST'])
@login_required
def tag_del(tag_id):
    # 删除标签
    tag = Tag.query.get(tag_id)
    if tag:
        db.session.delete(tag)
        db.session.commit()
        flash(f'{tag.name}删除成功')
        return redirect(url_for('admin.tag'))

