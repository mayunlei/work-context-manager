#!/usr/bin/env python3
"""
语音识别测试脚本
用于测试DashScope语音识别功能
"""

import os
import sys
from speech_recognition import SpeechRecognizer
import config

def test_asr():
    """测试语音识别功能"""
    print("🎤 语音识别测试")
    print("=" * 50)
    
    # 检查API配置
    if not config.DASHSCOPE_API_KEY:
        print("❌ 未设置 DASHSCOPE_API_KEY")
        print("请设置环境变量: export DASHSCOPE_API_KEY='your-key'")
        return False
    
    print(f"✅ 使用模型: {config.DASHSCOPE_ASR_MODEL}")
    
    # 创建语音识别器
    recognizer = SpeechRecognizer()
    
    # 测试音频文件路径
    test_audio_path = "test_audio.wav"
    
    if not os.path.exists(test_audio_path):
        print(f"❌ 测试音频文件不存在: {test_audio_path}")
        print("请创建一个测试音频文件或录制一段音频")
        return False
    
    # 读取测试音频
    try:
        with open(test_audio_path, 'rb') as f:
            audio_data = f.read()
        print(f"✅ 读取音频文件: {len(audio_data)} bytes")
    except Exception as e:
        print(f"❌ 读取音频文件失败: {e}")
        return False
    
    # 进行语音识别
    print("🔄 开始语音识别...")
    try:
        result = recognizer.transcribe_audio(audio_data)
        if result:
            print("✅ 识别成功!")
            print(f"识别结果: {result}")
            return True
        else:
            print("❌ 识别失败，未返回结果")
            return False
    except Exception as e:
        print(f"❌ 识别过程出错: {e}")
        return False

if __name__ == "__main__":
    success = test_asr()
    sys.exit(0 if success else 1) 