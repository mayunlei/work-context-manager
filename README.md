# 上下文切换器 (Context Switcher)

一个基于语音识别的项目上下文管理工具，帮助程序员在多个项目间快速切换并保存上下文信息。

## 功能特性

- 🎤 **语音输入**: 通过快捷键 `Cmd+Shift+E` 快速录音
- 🤖 **AI语音识别**: 支持OpenAI Whisper和阿里云DashScope
- 🧠 **智能合并**: 使用AI自动合并和整理上下文信息
- 📝 **Markdown格式**: 结构化的上下文记录
- 📊 **历史记录**: 完整的操作历史追踪
- 🖥️ **状态栏显示**: 实时显示录音状态
- 💾 **自动备份**: 支持上下文备份功能

## 安装

1. **克隆项目**:
```bash
git clone <repository-url>
cd context_switcher1
```

2. **安装依赖**:
```bash
pip install -r requirements.txt
```

3. **配置API密钥**:

### 方法1: 使用环境变量
```bash
# OpenAI配置
export OPENAI_API_KEY="your-openai-api-key"
export OPENAI_BASE_URL="https://api.openai.com/v1"

# 阿里云DashScope配置
export DASHSCOPE_API_KEY="your-dashscope-api-key"
export DASHSCOPE_ASR_MODEL="paraformer-v2"
export DASHSCOPE_LLM_MODEL="qwen-turbo"

# 上下文合并配置
export CONTEXT_MERGE_PROVIDER="openai"  # openai 或 dashscope
export CONTEXT_MERGE_MODEL="gpt-3.5-turbo"  # 或 qwen-turbo 等

# OSS配置（用于语音识别）
export OSS_ACCESS_KEY_ID="your-oss-access-key-id"
export OSS_ACCESS_KEY_SECRET="your-oss-access-key-secret"
export OSS_ENDPOINT="https://oss-cn-beijing.aliyuncs.com"
export OSS_BUCKET_NAME="your-bucket-name"
export OSS_BUCKET_DOMAIN="your-bucket-domain"
```

### 方法2: 使用.env文件（推荐）
```bash
# 复制配置文件示例
cp .env.example .env

# 编辑.env文件，填入你的API密钥
nano .env
```

## 使用方法

1. **启动程序**:
```bash
python main.py
```

2. **开始录音**: 按住 `Cmd+Shift+E` 开始录音（状态栏图标变红）
3. **停止录音**: 松开按键停止录音并自动处理
4. **查看结果**: 程序会自动将语音转换为文字并合并到上下文中

## 文件输出

程序会在桌面创建以下文件：

- `context_switcher_context.md` - 当前上下文文件
- `context_switcher_history.md` - 历史记录文件
- `context_backup_YYYYMMDD_HHMMSS.md` - 备份文件（手动创建）

## 上下文格式

每个项目按以下格式组织：

```markdown
## 项目名称

**更新时间**: 2024-01-01 12:00:00
**最终目标**: 项目的主要目标
**当前状态**: 当前进展状态
**Todo列表**:
- [ ] 任务1 (状态: 进行中, Block: 等待依赖)
- [x] 任务2 (已完成)

**当前Block点**: 描述当前阻碍
**解决Block后**: 下一步行动计划
```

## 状态栏菜单

- **备份上下文**: 创建带时间戳的备份文件
- **打开上下文文件**: 在默认编辑器中打开当前上下文
- **打开历史记录**: 查看所有历史记录
- **退出**: 关闭程序

## 配置选项

可以通过环境变量配置以下选项：

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `OPENAI_API_KEY` | OpenAI API密钥 | - |
| `OPENAI_BASE_URL` | OpenAI API地址 | https://api.openai.com/v1 |
| `DASHSCOPE_API_KEY` | 阿里云DashScope API密钥 | - |
| `DASHSCOPE_ASR_MODEL` | 语音识别模型 | paraformer-v2 |
| `DASHSCOPE_LLM_MODEL` | 文本生成模型 | qwen-turbo |
| `CONTEXT_MERGE_PROVIDER` | 上下文合并提供商 | openai |
| `CONTEXT_MERGE_MODEL` | 上下文合并模型 | gpt-3.5-turbo |
| `OSS_ACCESS_KEY_ID` | 阿里云OSS AccessKey ID | - |
| `OSS_ACCESS_KEY_SECRET` | 阿里云OSS AccessKey Secret | - |
| `OSS_ENDPOINT` | OSS服务端点 | https://oss-cn-beijing.aliyuncs.com |
| `OSS_BUCKET_NAME` | OSS存储桶名称 | - |
| `OSS_BUCKET_DOMAIN` | OSS存储桶域名 | - |

## 快捷键

- `Cmd+Shift+E`: 开始/停止录音

## 测试

### 测试OSS上传功能
```bash
python test_oss.py
```

### 测试语音识别功能
```bash
python test_asr.py
```

### 测试上下文合并功能
```bash
python test_merge.py
```

注意：需要先创建一个 `test_audio.wav` 文件用于测试。

## 故障排除

1. **权限问题**: 确保程序有麦克风访问权限
2. **API错误**: 检查API密钥是否正确设置
3. **网络问题**: 确保网络连接正常
4. **依赖问题**: 重新安装依赖 `pip install -r requirements.txt`
5. **语音识别失败**: 检查音频格式是否为WAV，采样率是否为16kHz

## 开发说明

项目结构：
```
├── main.py              # 主程序入口
├── config.py            # 配置文件
├── audio_recorder.py    # 音频录制模块
├── speech_recognition.py # 语音识别模块
├── context_manager.py   # 上下文管理模块
├── status_bar.py        # 状态栏模块
├── hotkey_manager.py    # 快捷键管理模块
└── requirements.txt     # Python依赖
```

## 许可证

MIT License 