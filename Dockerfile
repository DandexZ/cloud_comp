# 使用官方推荐标签
FROM gcc:latest

WORKDIR /app
COPY main.cpp .

# 安装编译依赖（如有需要）
RUN apt-get update && \
    apt-get install -y locales && \
    locale-gen zh_CN.UTF-8

# 编译
RUN g++ -o cloud_comp main.cpp

# 设置中文环境
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

CMD ["./cloud_comp"]