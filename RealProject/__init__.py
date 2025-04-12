import os
from flask import Flask


def create_app(test_config=None):
    #create and configure the app
    # instance_ralative_config设置为true则代表开启从文件加载配置，默认为false
    app = Flask(__name__, instance_relative_config=True)
    # app.config是调用flask类的config属性，该属性又被设置为一个config的类
    ##from_mapping是该类下的一个方法，用来更新默认配置，返回值为true
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        #加载实例配置
        app.config.from_pyfile('settings.py', silent=True)
    else:
        #加载测试配置
        app.config.from_mapping(test_config)

    #递归创建目录，确保项目文件存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    
    @app.route('/hello')
    def hello_world():
        return "<p>Hello, World!</p>"
    return app




