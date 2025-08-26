#!/bin/bash

# 上传wheel包到devpi服务器的脚本
# 使用方法: ./uploadwhl.sh

set -e  # 遇到错误时退出

echo "开始上传wheel包到devpi服务器..."

# 检查dist目录是否存在
if [ ! -d "dist" ]; then
    echo "错误: dist目录不存在，请先运行构建命令生成wheel包"
    exit 1
fi

# 检查dist目录是否为空
if [ -z "$(ls -A dist)" ]; then
    echo "错误: dist目录为空，请先运行构建命令生成wheel包"
    exit 1
fi

echo "连接到devpi服务器..."
devpi use http://devpiread:Devpiread123@10.12.0.78:13141/

echo "登录devpi服务器..."
devpi login root --password=Devpi@123

echo "上传到release仓库..."
devpi use root/release/+simple/
devpi upload --from-dir dist

echo "上传到dev仓库..."
devpi use root/dev/+simple/
devpi upload --from-dir dist

echo "上传完成！"