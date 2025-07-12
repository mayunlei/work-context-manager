#!/usr/bin/env python3
"""
上下文合并测试脚本
用于测试不同提供商的上下文合并功能
"""

import os
import sys
from speech_recognition import SpeechRecognizer
import config

def test_context_merge():
    """测试上下文合并功能"""
    print("🧠 上下文合并测试")
    print("=" * 50)
    
    # 检查配置
    print(f"提供商: {config.CONTEXT_MERGE_PROVIDER}")
    print(f"模型: {config.CONTEXT_MERGE_MODEL}")
    
    if config.CONTEXT_MERGE_PROVIDER.lower() == "openai" and not config.OPENAI_API_KEY:
        print("❌ 未设置 OPENAI_API_KEY")
        return False
    elif config.CONTEXT_MERGE_PROVIDER.lower() == "dashscope" and not config.DASHSCOPE_API_KEY:
        print("❌ 未设置 DASHSCOPE_API_KEY")
        return False
    
    # 创建语音识别器
    recognizer = SpeechRecognizer()
    
    # 测试数据
    existing_context = """# 上下文切换器

## 项目A

**更新时间**: 2024-01-01 12:00:00
**最终目标**: 完成语音识别功能
**当前状态**: 开发中
**Todo列表**:
- [x] 基础录音功能
- [ ] 语音识别集成
- [ ] 上下文合并

**当前Block点**: 等待API密钥配置
**解决Block后**: 继续开发语音识别模块
"""
    
    new_content = "语音识别功能已经完成，现在需要测试上下文合并功能，确保新内容能够正确合并到现有项目中。"
    
    print("📝 现有上下文:")
    print(existing_context)
    print("\n📝 新内容:")
    print(new_content)
    print("\n🔄 开始合并...")
    
    try:
        merged_context = recognizer.merge_context(existing_context, new_content)
        print("✅ 合并成功!")
        print("\n📝 合并结果:")
        print(merged_context)
        return True
    except Exception as e:
        print(f"❌ 合并失败: {e}")
        return False

if __name__ == "__main__":
    success = test_context_merge()
    sys.exit(0 if success else 1) 