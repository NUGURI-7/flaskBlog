from datetime import datetime
from RealProject import db
from enum import IntEnum
from sqlalchemy.dialects.mysql import LONGTEXT

class BaseModel(db.Model):
    """
    基础模型类
    """
    __abstract__ = True  # 声明为抽象类
    
    add_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, )  # 添加时间
    pub_date = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow,nullable=False)  # 更新时间

class Category(BaseModel):
    """
    分类模型
    """
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(128), nullable=False)  # 分类名称
    icon = db.Column(db.String(128), nullable=True)  # 分类图标
    post = db.relationship('Post', backref='category', lazy=True)  # 反向关系，获取分类下的所有文章

    def __repr__(self):
        return '<Category %r>' % self.name
    
class PostPublishType(IntEnum):
    """
    文章发布类型
    """
    draft = 1 #草稿
    show = 2 #发布
#多对多关系帮助器表
tags = db.Table('tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),  # 文章ID
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)  # 标签ID
)


class Post(BaseModel):
    """
    文章模型
    """
   
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(128), nullable=False)  # 发布类型标题
    desc = db.Column(db.String(128), nullable=True)  # 发布类型描述
    content = db.Column(LONGTEXT, nullable=False)  # 发布类型内容
    has_type = db.Column(db.Enum(PostPublishType), server_default='show', nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)  # 分类ID
    #多对多关系
    tags = db.relationship('Tag', secondary=tags, 
                           backref=db.backref('post', lazy=True),
                             lazy='subquery')  # 标签ID

    def __repr__(self):
        return '<Post %r>' % self.title




class Tag(BaseModel):
    """
    标签模型
    """
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(128), nullable=False, unique=True)  # 标签名称
    
    def __repr__(self):
        return self.name


































