 #!/bin/bash

echo "🚀 上下文切换器安装脚本"
echo "=========================="

# 检查Python版本
python_version=$(python3 --version 2>&1 | grep -o '[0-9]\+\.[0-9]\+')
echo "检测到Python版本: $python_version"

# 使用更简单的版本比较方法
major_version=$(echo $python_version | cut -d. -f1)
minor_version=$(echo $python_version | cut -d. -f2)

if [[ $major_version -gt 3 ]] || [[ $major_version -eq 3 && $minor_version -ge 8 ]]; then
    echo "✅ Python版本检查通过: $python_version"
else
    echo "❌ 需要Python 3.8或更高版本，当前版本: $python_version"
    exit 1
fi

# 检查conda是否可用
if command -v conda &> /dev/null; then
    echo "📦 使用conda环境: py312"
    
    # 检查环境是否存在
    if conda env list | grep -q "py312"; then
        echo "✅ conda环境 py312 已存在"
    else
        echo "📦 创建conda环境 py312..."
        conda create -n py312 python=3.12 -y
        echo "✅ conda环境创建成功"
    fi
    
    # 激活conda环境并安装依赖
    echo "📦 激活conda环境并安装依赖..."
    conda activate py312
    pip install -r requirements.txt
else
    echo "⚠️  conda未安装或不在PATH中"
    echo ""
    echo "请选择安装方式："
    echo "1. 使用系统Python (需要 --break-system-packages)"
    echo "2. 创建虚拟环境"
    echo "3. 安装conda"
    echo ""
    read -p "请选择 (1/2/3): " choice
    
    case $choice in
        1)
            echo "📦 使用系统Python安装..."
            pip3 install -r requirements.txt --break-system-packages
            ;;
        2)
            echo "📦 创建Python虚拟环境..."
            python3 -m venv venv
            source venv/bin/activate
            pip install -r requirements.txt
            ;;
        3)
            echo "📦 安装Miniconda..."
            echo "请访问 https://docs.conda.io/en/latest/miniconda.html 下载并安装Miniconda"
            echo "安装完成后重新运行此脚本"
            exit 1
            ;;
        *)
            echo "❌ 无效选择"
            exit 1
            ;;
    esac
fi

if [ $? -eq 0 ]; then
    echo "✅ 依赖安装成功"
else
    echo "❌ 依赖安装失败，请检查网络连接"
    exit 1
fi

# 创建配置文件示例
echo "📝 创建配置文件示例..."
cat > .env.example << EOF
# OpenAI配置
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1

# 阿里云DashScope配置
DASHSCOPE_API_KEY=your-dashscope-api-key-here
DASHSCOPE_ASR_MODEL=paraformer-v2
DASHSCOPE_LLM_MODEL=qwen-turbo

# 上下文合并配置
CONTEXT_MERGE_PROVIDER=openai
CONTEXT_MERGE_MODEL=gpt-3.5-turbo

# Gemini配置（用于上下文合并）
GOOGLE_CLOUD_PROJECT=your-google-cloud-project-id-here

# 阿里云OSS配置（用于语音识别）
OSS_ACCESS_KEY_ID=your-oss-access-key-id-here
OSS_ACCESS_KEY_SECRET=your-oss-access-key-secret-here
OSS_ENDPOINT=https://oss-cn-beijing.aliyuncs.com
OSS_BUCKET_NAME=your-bucket-name-here
OSS_BUCKET_DOMAIN=your-bucket-domain-here
EOF

echo "✅ 配置文件示例已创建: .env.example"

# 检查麦克风权限
echo "🎤 检查麦克风权限..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "请确保在系统偏好设置 > 安全性与隐私 > 麦克风中允许Python访问麦克风"
    echo "如果程序无法录音，请手动授予权限"
fi

echo ""
echo "🎉 安装完成！"
echo ""
echo "下一步："
echo "1. 复制 .env.example 为 .env 并填入你的API密钥"
echo "2. 运行 './start.sh' 启动程序"
echo "3. 使用 Cmd+Shift+E 开始录音"
echo ""
echo "或者直接运行: python main.py"
echo ""
echo "更多信息请查看 README.md" 