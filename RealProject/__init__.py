import os
from RealProject.settings import BASE_DIR
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


#操作数据库
db = SQLAlchemy()
migrate = Migrate() #数据库迁移


def create_app(test_config=None):
    #create and configure the app
    # instance_ralative_config设置为true则代表开启从文件加载配置，默认为false
    app = Flask(__name__, instance_relative_config=True)
    
    # app.config.from_mapping(
    #     SECRET_KEY='dev',
    #     DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    # )

    if test_config is None:
        CONFIG_PATH = BASE_DIR / 'RealProject/settings.py'
        app.config.from_pyfile(CONFIG_PATH, silent=True)
    else:
        # test_config为一个字典
        app.config.from_mapping(test_config)


    db.init_app(app) #初始化数据库,工厂函数中注册
    migrate.init_app(app, db) #初始化数据库迁移


    #引入blog的视图文件
    from app.blog import views as blog
    app.register_blueprint(blog.bp)
    from app.auth import views as auth
    app.register_blueprint(auth.bp) 
    from app.admin import views as admin
    app.register_blueprint(admin.bp)

    # url 引入
    app.add_url_rule('/', endpoint='index', view_func=blog.index) #注册路由
    #注册数据库
    from app.blog import models 
    from app.auth import models 

    #引入上下文
    app.context_processor(inject_category) #注册上下文处理器

    return app


def inject_category():
    # 上下文处理器回调函数
    """
    context_processor上下文处理器在呈现模板之前运行，并且能够将新值注入模板上下文。上下文处理器是返回字典的函数。
    然后，对于应用程序中的所有模板，此字典的键和值将与模板上下文合并：
    """
    from app.blog.models import Category
    categories = Category.query.limit(6).all()
    return dict(categories=categories)  # 返回字典类型的对象
