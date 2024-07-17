# 使用 Alpine Linux 作為基礎映像
FROM python:3.9-alpine

# 設置工作目錄
WORKDIR /app

# 複製應用程序代碼到容器中
COPY app.py /app/

# 安裝 Flask 框架和相關依賴項
RUN apk --no-cache add build-base \
    && pip install --no-cache-dir flask \
    && apk del build-base \
    && rm -rf /var/cache/apk/*
RUN mkdir /app/image
# 暴露 5000 端口
EXPOSE 5000
VOLUME ["/app/image"]

# 定義容器啟動命令
CMD ["flask", "run", "--host=0.0.0.0"]