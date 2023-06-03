import os
import random
from flask import Flask, send_file, abort

app = Flask(__name__)

# 設置圖片目錄
IMAGE_DIR = '/image'
MIME_TYPES = {
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'webp': 'image/webp'
}

@app.route('/picbed/<album_name>')
def random_image(album_name):
    # 檢查目錄是否存在
    album_path = os.path.join(IMAGE_DIR, album_name)
    if not os.path.isdir(album_path):
        abort(404)
    # 讀取圖片列表
    image_list = os.listdir(album_path)
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

if __name__ == '__main__':
    app.run()