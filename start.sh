#!/bin/bash

echo "🎤 启动上下文切换器..."

# 检查.env文件是否存在
if [ -f ".env" ]; then
    echo "📄 加载.env配置文件..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# 检查是否设置了API密钥
if [[ -z "$OPENAI_API_KEY" && -z "$DASHSCOPE_API_KEY" ]]; then
    echo "⚠️  警告: 未设置API密钥"
    echo "请设置以下环境变量之一："
    echo "  export OPENAI_API_KEY='your-openai-key'"
    echo "  export DASHSCOPE_API_KEY='your-dashscope-key'"
    echo ""
    echo "或者创建 .env 文件并运行: ./start.sh"
    echo ""
    read -p "是否继续启动程序？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# 检查conda环境
if command -v conda &> /dev/null; then
    echo "🔧 激活conda环境 py312..."
    conda activate py312
    python main.py
else
    echo "⚠️  conda未安装或不在PATH中"
    exit 1
fi 