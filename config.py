import os
from pathlib import Path
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

# API配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")

# DashScope配置
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
DASHSCOPE_ASR_MODEL = os.getenv("DASHSCOPE_ASR_MODEL", "paraformer-v2")
DASHSCOPE_LLM_MODEL = os.getenv("DASHSCOPE_LLM_MODEL", "qwen-turbo")

# 上下文合并配置
CONTEXT_MERGE_PROVIDER = os.getenv("CONTEXT_MERGE_PROVIDER", "openai")  # openai, dashscope, 或 gemini
CONTEXT_MERGE_MODEL = os.getenv("CONTEXT_MERGE_MODEL", "gpt-3.5-turbo")  # 默认使用OpenAI

# Gemini配置
GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")

# OSS配置
OSS_ACCESS_KEY_ID = os.getenv("OSS_ACCESS_KEY_ID", "")
OSS_ACCESS_KEY_SECRET = os.getenv("OSS_ACCESS_KEY_SECRET", "")
OSS_ENDPOINT = os.getenv("OSS_ENDPOINT", "https://oss-cn-beijing.aliyuncs.com")
OSS_BUCKET_NAME = os.getenv("OSS_BUCKET_NAME", "")
OSS_BUCKET_DOMAIN = os.getenv("OSS_BUCKET_DOMAIN", "")

# 文件路径配置
DESKTOP_PATH = Path.home() / "Desktop"
CONTEXT_FILE = DESKTOP_PATH / "context_switcher_context.md"
HISTORY_FILE = DESKTOP_PATH / "context_switcher_history.md"

# 录音配置
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_SIZE = 1024

# 快捷键配置
RECORD_HOTKEY = {'cmd', 'shift', 'e'} 