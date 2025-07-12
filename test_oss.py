#!/usr/bin/env python3
"""
OSS上传测试脚本
用于测试OSS配置和上传功能
"""

import os
import sys
from oss_uploader import OSSUploader
import config

def test_oss():
    """测试OSS上传功能"""
    print("☁️  OSS上传测试")
    print("=" * 50)
    
    # 检查OSS配置
    required_vars = [
        'OSS_ACCESS_KEY_ID',
        'OSS_ACCESS_KEY_SECRET', 
        'OSS_BUCKET_NAME'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not getattr(config, var, None):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ 缺少OSS配置: {', '.join(missing_vars)}")
        print("请设置相应的环境变量")
        return False
    
    print("✅ OSS配置检查通过")
    
    # 创建OSS上传器
    uploader = OSSUploader()
    
    if not uploader.is_configured():
        print("❌ OSS客户端初始化失败")
        return False
    
    print("✅ OSS客户端初始化成功")
    
    # 创建测试音频数据
    test_audio_data = b"RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x44\xAC\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00"
    
    print("📤 上传测试音频...")
    
    # 上传测试音频
    try:
        oss_url, object_key = uploader.upload_audio(test_audio_data, "wav")
        if oss_url:
            print("✅ 上传成功!")
            print(f"OSS URL: {oss_url}")
            print(f"Object Key: {object_key}")
            
            # 测试删除功能
            print("🗑️  测试删除功能...")
            if uploader.delete_audio(object_key):
                print("✅ 删除成功!")
            else:
                print("❌ 删除失败")
            
            return True
        else:
            print("❌ 上传失败")
            return False
    except Exception as e:
        print(f"❌ 上传过程出错: {e}")
        return False

if __name__ == "__main__":
    success = test_oss()
    sys.exit(0 if success else 1) 