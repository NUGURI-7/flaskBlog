import os
import uuid
from RealProject.settings import BASE_DIR
from werkzeug.utils import secure_filename


def _file_path(directory_name):
   #判断该路径是否存在
    file_path = BASE_DIR / f'app/admin/static/{directory_name}'
    if os.path.exists(file_path) is False:
        os.makedirs(file_path)
    return file_path   

def update_filename(f):
    #修改文件名称
    names = list(os.path.splitext(secure_filename(f.filename))) #拆分文件名
    names[0] = ''.join(str(uuid.uuid4()).split('-'))
    return ''.join(names) #返回文件名


def upload_file_path(f, directory_name):
    #处理过的图片保存路径
    file_path = _file_path(directory_name)
    filename = update_filename(f)
    return file_path / filename, filename
    