import os
import random
from flask import Flask, send_file, abort, request
import uuid
import re

app = Flask(__name__)

# 設置圖片目錄
HOST = os.environ.get('HOST', 'http://localhost:5000')
TOKEN = os.environ.get('TOKEN', 'token')
ALLOWED_FILENAME_PATTERN = r'^[\w\-_\.]+$'
IMAGE_DIR = 'image'
MIME_TYPES = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'webp': 'image/webp'
}

@app.route('/picbed/<album_name>/<image_name>')
def staticImage(album_name,image_name):
    # 檢查目錄是否存在
    album_path = os.path.join(IMAGE_DIR, album_name)
    if not os.path.isdir(album_path):
        abort(404)
    # 讀取圖片列表
    image_list = os.listdir(album_path)
    if len(image_list) == 0:
        abort(404)
    # 獲取圖片檔案的副檔名
    ext = os.path.splitext(image_name)[1][1:].lower()
    # 檢查副檔名是否為支援的格式
    if ext not in MIME_TYPES:
        abort(500)
    # 構造圖片路徑
    image_path = os.path.join(album_path, image_name)
    # 回傳圖片，設置正確的 MIME 類型
    mimetype = MIME_TYPES.get(ext, 'application/octet-stream')
    return send_file(image_path, mimetype=mimetype)

@app.route('/picbed/<album_name>')
def random_image(album_name):
    # 檢查目錄是否存在
    album_path = os.path.join(IMAGE_DIR, album_name)
    if not os.path.isdir(album_path):
        abort(404)
    # 讀取圖片列表
    image_list = os.listdir(album_path)
    if len(image_list) == 0:
        abort(404)
    # 隨機選擇一張圖片
    image_name = random.choice(image_list)
    # 獲取圖片檔案的副檔名
    ext = os.path.splitext(image_name)[1][1:].lower()
    # 檢查副檔名是否為支援的格式
    if ext not in MIME_TYPES:
        abort(500)
    # 構造圖片路徑
    image_path = os.path.join(album_path, image_name)
    # 回傳圖片，設置正確的 MIME 類型
    mimetype = MIME_TYPES.get(ext, 'application/octet-stream')
    return send_file(image_path, mimetype=mimetype)

@app.route('/picbed/upload/<album_name>', methods=['POST'])
def upload_file(album_name):
    uploaded_files = []
    auth = request.headers.get('Authorization')
    if auth != TOKEN:
        return "Unauthorized", 401
    files = request.files.getlist('files')
    for file in files:
        # 檢查文件類型是否允許
        if file.content_type not in MIME_TYPES.values():
            abort(400)
        if not re.match(ALLOWED_FILENAME_PATTERN, file.filename):
            abort(400)
        # 生成唯一的文件名
        filename = str(uuid.uuid4())
        file_extension = os.path.splitext(file.filename)[1]
        filename += file_extension
        
        # 保存文件到本地
        save_path = os.path.join(IMAGE_DIR,album_name, filename)
        # 如果目錄不存在，則創建目錄
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        file.save(save_path)
        uploaded_files.append(f'{HOST}/picbed/{album_name}/{filename}')
    
    return {
        "random": f"{HOST}/picbed/{album_name}",
        "uploaded": uploaded_files
    }

if __name__ == '__main__':
    app.run()