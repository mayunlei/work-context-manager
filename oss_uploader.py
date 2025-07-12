import oss2
import uuid
import time
from datetime import datetime, timedelta
from typing import Optional
import config

class OSSUploader:
    def __init__(self):
        self.access_key_id = config.OSS_ACCESS_KEY_ID
        self.access_key_secret = config.OSS_ACCESS_KEY_SECRET
        self.endpoint = config.OSS_ENDPOINT
        self.bucket_name = config.OSS_BUCKET_NAME
        self.bucket_domain = config.OSS_BUCKET_DOMAIN
        
        # 初始化OSS客户端
        if all([self.access_key_id, self.access_key_secret, self.endpoint, self.bucket_name]):
            self.auth = oss2.Auth(self.access_key_id, self.access_key_secret)
            self.bucket = oss2.Bucket(self.auth, self.endpoint, self.bucket_name)
        else:
            self.bucket = None
            print("警告: OSS配置不完整，将使用本地文件路径")
    
    def upload_audio(self, audio_data: bytes, file_extension: str = "wav") -> tuple[Optional[str], Optional[str]]:
        """上传音频文件到OSS并返回(签名URL, object_key)"""
        if not self.bucket:
            print("OSS未配置，无法上传文件")
            return None, None
        
        try:
            # 生成唯一的文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            object_key = f"audio/{timestamp}_{unique_id}.{file_extension}"
            
            # 上传文件到OSS
            print(f"上传音频文件到OSS: {object_key}")
            result = self.bucket.put_object(object_key, audio_data)
            
            if result.status == 200:
                # 生成带签名的URL，有效期1小时
                expires = int(time.time()) + 3600  # 1小时后过期
                signed_url = self.bucket.sign_url('GET', object_key, expires)
                
                print(f"文件上传成功，签名URL: {signed_url}")
                return signed_url, object_key
            else:
                print(f"文件上传失败，状态码: {result.status}")
                return None, None
                
        except Exception as e:
            print(f"OSS上传失败: {e}")
            return None, None
    
    def delete_audio(self, object_key: str) -> bool:
        """删除OSS上的音频文件"""
        if not self.bucket:
            return False
        
        try:
            self.bucket.delete_object(object_key)
            print(f"删除OSS文件: {object_key}")
            return True
        except Exception as e:
            print(f"删除OSS文件失败: {e}")
            return False
    
    def is_configured(self) -> bool:
        """检查OSS是否已配置"""
        return self.bucket is not None 