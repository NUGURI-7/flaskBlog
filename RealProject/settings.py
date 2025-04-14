from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

SECRET_KEY = '1%#@!$%&*()_+1234567890-=qwertyuiop[]{};:\'",.<>?/'

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:020121@localhost:3306/flaskblog'

SQLALCHEMY_COMMIT_ON_TEARDOWN = True
# 每次请求结束后自动提交数据库的变更
SQLALCHEMY_TRACK_MODIFICATIONS = True
