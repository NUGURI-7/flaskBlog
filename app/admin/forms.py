from flask_wtf import FlaskForm
from wtforms import (StringField, RadioField, TextAreaField, SelectField,
                     SelectMultipleField, BooleanField, PasswordField)
from wtforms.validators import DataRequired, Length
from app.blog.models import PostPublishType

class CategoryCreateForm(FlaskForm):
    # 分类表单
    name = StringField('分类名称', validators=[
        DataRequired(message="不能为空"), 
        Length(max=128, message="不符合字数要求！")
    ])
    icon = StringField('分类图标', validators=[ 
        Length(max=256, message="不符合字数要求！")
    ])



class PostForm(FlaskForm):
    # 添加文章表单
    title = StringField('标题', validators=[
        DataRequired(message="不能为空"), 
        Length(max=128, message="不符合字数要求！")
    ])
    desc = StringField('描述', validators=[
        DataRequired(message="不能为空"), 
        Length(max=200, message="不符合字数要求！")
    ])
    has_type = RadioField('发布状态', 
        choices=(PostPublishType.draft.name, PostPublishType.show.name), 
        default=PostPublishType.show.name)
    category_id = SelectField(
        '分类', 
        choices=None, 
        coerce=int,
        validators=[
            DataRequired(message="不能为空"),
        ]
    )
    content = TextAreaField('文章详情', 
        validators=[DataRequired(message="不能为空")]
    )
    tags = SelectMultipleField('文章标签', choices=None, coerce=int)


class TagForm(FlaskForm):
    # 标签表单
    name = StringField('标签名称', validators=[
        DataRequired(message="不能为空"), 
        Length(max=128, message="不符合字数要求！")
    ])    


from flask_wtf.file import FileField, FileAllowed, FileRequired,FileSize

class CreateUserForm(FlaskForm):
    # 用户表单
    username = StringField('用户名', validators=[
        DataRequired(message="不能为空"), 
        Length(max=32, message="不符合字数要求！")
    ])
    password = PasswordField('密码', validators=[
        # DataRequired(message="不能为空"), 
        Length(max=32, message="不符合字数要求！")
    ], description='修改用户信息时，留空则代表不修改')
    avatar = FileField('头像', validators=[
        # FileRequired('未选择文件'),
        FileAllowed(['jpg', 'png','gif'], '只能上传jpg/png/gif格式的文件'),
        FileSize(max_size=2*1024*1024, message='文件过大，不能超过2MB')
        ],description='修改用户头像时，留空则代表不修改')
    is_super_user = BooleanField('是否为超级管理员')
    is_active = BooleanField('是否为活跃用户',default=True)
    is_staff = BooleanField("是否锁定")