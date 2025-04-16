from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class CategoryCreateForm(FlaskForm):
    # 分类表单
    name = StringField('分类名称', validators=[
        DataRequired(message="不能为空"), 
        Length(max=128, message="不符合字数要求！")
    ])
    icon = StringField('分类图标', validators=[ 
        Length(max=256, message="不符合字数要求！")
    ])

