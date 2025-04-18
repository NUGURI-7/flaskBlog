from flask import(Blueprint, render_template, request, 
                  redirect, url_for, flash, session)
from .models import Post, Category, Tag


bp = Blueprint('blog',__name__, url_prefix='/blog',
               static_folder='static', template_folder='templates')


def index():
    """
    博客首页视图函数
    """
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.order_by(
        -Post.add_date).paginate(page=page, per_page=2, error_out=False)
    post_list = pagination.items

    import random
    imgs = ['https://live.staticflickr.com/65535/52606321289_1c77c0892d_b.jpg', 
            'https://pic.52112.com/180324/180324_111/YtrXq712DT_small.jpg',
            'https://pic.52112.com/2020/04/13/JPG-200413_422/1JkJ54eoiT_small.jpg', 
            'https://p1.ssl.qhimg.com/t01e86de743eb8246ad.jpg', 
            # 'https://bkimg.cdn.bcebos.com/pic/77094b36acaf2edda3cc3b5e9a5a16e93901213f3578'
            ]

    for post in post_list:
        # 随机选择一张图片
        post.img = random.sample(imgs, 1)[0]


    # posts = [1,2,3,4,5,6,]
    return render_template('index.html', posts=post_list, pagination=pagination)

#文章列表页
@bp.route('/category/<int:cate_id>')
def category(cate_id):
    """
    博客分类视图函数
    """
    cate =Category.query.get(cate_id)
    page = request.args.get('page', 1, type=int)
    pagination = Post.query.filter(Post.category_id==cate_id).paginate(page=page, per_page=2, error_out=False)
    post_list = pagination.items
    return render_template('cate_list.html', cate=cate, post_list=post_list, 
                            cate_id=cate_id, pagination=pagination)    


#文章详情页
@bp.route('/category/<int:cate_id>/<int:post_id>', methods=['GET', 'POST'])
def detail(cate_id, post_id):
    """
    博客文章详情视图函数
    """
    cate = Category.query.get(cate_id)
    post = Post.query.get_or_404(post_id)
    #上一篇
    prev_post = Post.query.filter(Post.id < post.id).order_by(-Post.id).first() 
    #下一篇
    next_post = Post.query.filter(Post.id > post.id).order_by(Post.id).first()
    return render_template('detail.html', cate=cate, post=post,prev_post=prev_post, next_post=next_post)                            