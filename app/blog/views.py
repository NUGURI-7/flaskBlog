from flask import(Blueprint, render_template, request, 
                  redirect, url_for, flash, session)
from .models import Post


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