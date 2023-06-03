# PicBed
PicBed 是一個基於Python Flask隨機圖床API，並且以目錄分類項目，支持 Docker 容器化。

## 開始使用
### 添加圖片
在 `image` 目錄底下新增相簿目錄，通過訪問 `http://localhost:5000/picbed/{album}` 即可或的相簿中隨機圖片
### 通過python運行
1. clone專案
2. 安裝依賴
```
pip install flask
```
3. 啟動flask
```
flask run --host=0.0.0.0
```
4. 訪問 [http://localhost:5000](http://localhost:5000)

### 通過docker運行
```bash
docker build -t picbed .
docker run \
  --name picbed \
  --restart always \
  -v /path/to/image:/image \
  -p 5000:5000 \
  picbed
```

### 通過docker-compose運行
1. 編輯docker-compose.yaml，調整volumes
2. 部屬容器
```
docker-compose up -d --build
```

這個指令會建立一個名為 `picbed` 的 Docker 映像檔，然後創建一個名為 `picbed` 的容器並運行它。您可以通過瀏覽器訪問 `http://localhost:5000` 來訪問 PicBed。

## 授權協議

PicBed 是在 MIT 授權協議下發布的。詳細信息請參見 [LICENSE](LICENSE) 文件。
