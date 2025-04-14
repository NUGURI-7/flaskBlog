from flask import Blueprint, render_template, request, redirect, url_for, flash, session


bp = Blueprint('blog',__name__, url_prefix='/blog',
               static_folder='static', template_folder='templates')


def index():

    posts = [1,2,3,4,5,6,]
    return render_template('index.html', posts=posts)