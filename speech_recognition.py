import openai
import dashscope
import tempfile
import os
from typing import Optional
import config
from oss_uploader import OSSUploader
from datetime import datetime

class SpeechRecognizer:
    def __init__(self):
        # 初始化OpenAI客户端（用于上下文合并）
        self.openai_client = openai.OpenAI(
            api_key=config.OPENAI_API_KEY,
            base_url=config.OPENAI_BASE_URL
        )
        
        # 设置DashScope API密钥
        if config.DASHSCOPE_API_KEY:
            dashscope.api_key = config.DASHSCOPE_API_KEY
        
        # 初始化OSS上传器
        self.oss_uploader = OSSUploader()
    
    def transcribe_audio(self, audio_data: bytes) -> Optional[str]:
        """将音频数据转换为文字"""
        try:
            # 使用DashScope进行语音识别
            if config.DASHSCOPE_API_KEY:
                return self._transcribe_with_dashscope(audio_data)
            else:
                # 如果没有DashScope密钥，回退到OpenAI
                return self._transcribe_with_openai(audio_data)
        except Exception as e:
            print(f"语音识别失败: {e}")
            return None
    
    def _transcribe_with_dashscope(self, audio_data: bytes) -> Optional[str]:
        """使用DashScope进行语音识别"""
        oss_url = None
        object_key = None
        
        try:
            # 上传音频到OSS
            if self.oss_uploader.is_configured():
                print("上传音频到OSS...")
                oss_url, object_key = self.oss_uploader.upload_audio(audio_data, "wav")
                if not oss_url:
                    print("OSS上传失败，尝试使用本地文件")
                    return self._transcribe_with_local_file(audio_data)
            else:
                print("OSS未配置，使用本地文件")
                return self._transcribe_with_local_file(audio_data)
            
            # 使用异步语音识别API
            print("开始语音识别...")
            task_response = dashscope.audio.asr.Transcription.async_call(
                model=config.DASHSCOPE_ASR_MODEL,
                file_urls=[oss_url],
                language_hints=['zh', 'en']
            )
            
            # 等待识别完成
            transcription_response = dashscope.audio.asr.Transcription.wait(
                task=task_response.output.task_id
            )
            
            if transcription_response.status_code == 200:
                # 提取识别的文本
                print("识别结果:", transcription_response.output)
                results = transcription_response.output.get('results', [])
                if results:
                    # 获取第一个结果的转录URL
                    url = results[0].get('transcription_url')
                    if url:
                        # 读取转录结果
                        print("转录URL:", url)
                        import json
                        from urllib import request
                        result = json.loads(request.urlopen(url).read().decode('utf8'))
                        print("转录结果:", result)
                        
                        # 根据新的结果格式提取文本
                        if 'transcripts' in result and result['transcripts']:
                            # 获取第一个transcript
                            transcript = result['transcripts'][0]
                            if 'text' in transcript:
                                text = transcript['text']
                                print("识别文本:", text)
                                return text
                            elif 'sentences' in transcript and transcript['sentences']:
                                # 从sentences中提取文本
                                sentences = transcript['sentences']
                                text = ' '.join([s.get('text', '') for s in sentences])
                                print("识别文本:", text)
                                return text
                        
                        # 如果没有找到transcripts，尝试其他字段
                        if 'text' in result:
                            return result['text']
                
                print("未找到转录结果")
                return None
                
                print("未找到转录结果")
                return None
            else:
                print(f"DashScope API错误: {transcription_response.output.message}")
                return None
                
        except Exception as e:
            print(f"DashScope语音识别失败: {e}")
            return None
        finally:
            # 删除OSS文件
            if object_key:
                print(f"清理OSS文件: {object_key}")
                self.oss_uploader.delete_audio(object_key)
    
    def _transcribe_with_local_file(self, audio_data: bytes) -> Optional[str]:
        """使用本地文件进行语音识别（备用方案）"""
        try:
            # 创建临时文件保存音频
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_file_path = temp_file.name
            
            # 使用本地文件路径（仅用于测试，生产环境需要OSS）
            task_response = dashscope.audio.asr.Transcription.async_call(
                model=config.DASHSCOPE_ASR_MODEL,
                file_urls=[temp_file_path],
                language_hints=['zh', 'en']
            )
            
            # 等待识别完成
            transcription_response = dashscope.audio.asr.Transcription.wait(
                task=task_response.output.task_id
            )
            
            # 清理临时文件
            os.unlink(temp_file_path)
            
            if transcription_response.status_code == 200:
                # 提取识别的文本
                results = transcription_response.output.get('results', [])
                if results:
                    url = results[0].get('transcription_url')
                    if url:
                        import json
                        from urllib import request
                        result = json.loads(request.urlopen(url).read().decode('utf8'))
                        
                        # 根据新的结果格式提取文本
                        if 'transcripts' in result and result['transcripts']:
                            # 获取第一个transcript
                            transcript = result['transcripts'][0]
                            if 'text' in transcript:
                                return transcript['text']
                            elif 'sentences' in transcript and transcript['sentences']:
                                # 从sentences中提取文本
                                sentences = transcript['sentences']
                                text = ' '.join([s.get('text', '') for s in sentences])
                                return text
                        
                        # 如果没有找到transcripts，尝试其他字段
                        if 'text' in result:
                            return result['text']
                
                return None
            else:
                print(f"本地文件识别失败: {transcription_response.output.message}")
                return None
                
        except Exception as e:
            print(f"本地文件识别失败: {e}")
            return None
    
    def _transcribe_with_openai(self, audio_data: bytes) -> Optional[str]:
        """使用OpenAI进行语音识别（备用方案）"""
        try:
            response = self.openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=("audio.wav", audio_data, "audio/wav"),
                language="zh"  # 支持中文
            )
            return response.text
        except Exception as e:
            print(f"OpenAI语音识别失败: {e}")
            return None
    
    def merge_context(self, existing_context: str, new_content: str) -> str:
        """使用AI合并上下文"""
        try:
            prompt = f"""
你会获得一个项目的新进展，请你根据新的描述信息，提取出所属项目，然后提取出其中提到的目标、当前状态、todo、block点等信息(如果没有，则无需合并）。
然后将新的内容与现有的上下文进行智能合并。保持markdown格式，按项目分组。请注意你不能发明新的内容，只能按照原始的新旧内容合并在一起，如果新旧内容存在冲突条目，则用新内容覆盖旧内容。

现有项目信息：
{existing_context}

更新项目信息：
{new_content}

请按照以下格式合并：
- 每个项目使用二级标题（## 项目名）
- 从新内容中整理出：更新时间、最终目标、当前状态、todo列表、block点
- 如果新内容涉及已有项目，请更新该项目的信息
- 如果是新项目，请创建新的项目段落
- 保持时间顺序和逻辑性

当前时间:
{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

请返回合并后的完整markdown内容：
"""
            
            # 根据配置选择提供商
            if config.CONTEXT_MERGE_PROVIDER.lower() == "dashscope":
                return self._merge_with_dashscope(prompt)
            elif config.CONTEXT_MERGE_PROVIDER.lower() == "gemini":
                return self._merge_with_gemini(prompt)
            else:
                return self._merge_with_openai(prompt)
                
        except Exception as e:
            print(f"上下文合并失败: {e}")
            # 如果AI合并失败，简单拼接
            return f"{existing_context}\n\n## 新内容\n{new_content}"
    
    def _merge_with_openai(self, prompt: str) -> str:
        """使用OpenAI合并上下文"""
        try:
            response = self.openai_client.chat.completions.create(
                model=config.CONTEXT_MERGE_MODEL,
                messages=[
                    {"role": "system", "content": "你是一个专业的上下文管理助手，擅长整理和合并项目信息。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI上下文合并失败: {e}")
            raise e
    
    def _merge_with_dashscope(self, prompt: str) -> str:
        """使用DashScope合并上下文"""
        try:
            response = dashscope.Generation.call(
                model=config.CONTEXT_MERGE_MODEL,
                messages=[
                    {"role": "system", "content": "你是一个专业的上下文管理助手，擅长整理和合并项目信息。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            if response.status_code == 200:
                print(response.output)
                return response.output.text
            else:
                print(f"DashScope上下文合并失败: {response.message}")
                raise Exception(f"DashScope API错误: {response.message}")
                
        except Exception as e:
            print(f"DashScope上下文合并失败: {e}")
            raise e
    
    def _merge_with_gemini(self, prompt: str) -> str:
        """使用Gemini命令行合并上下文"""
        try:
            import subprocess
            import json
            
            # 检查是否设置了Google Cloud项目
            if not config.GOOGLE_CLOUD_PROJECT:
                raise Exception("未设置 GOOGLE_CLOUD_PROJECT 环境变量")
            
            # 设置环境变量
            env = os.environ.copy()
            env['GOOGLE_CLOUD_PROJECT'] = config.GOOGLE_CLOUD_PROJECT
            
            # 构建gemini命令
            cmd = ['gemini', '-p', prompt]
            
            print(f"调用Gemini命令: {' '.join(cmd)}")
            
            # 执行命令
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                env=env,
                timeout=60  # 60秒超时
            )
            
            if result.returncode == 0:
                # 成功执行
                response_text = result.stdout.strip()
                print(f"Gemini响应: {response_text[:100]}...")
                return response_text
            else:
                # 执行失败
                error_msg = result.stderr.strip()
                print(f"Gemini命令执行失败: {error_msg}")
                raise Exception(f"Gemini命令执行失败: {error_msg}")
                
        except subprocess.TimeoutExpired:
            print("Gemini命令执行超时")
            raise Exception("Gemini命令执行超时")
        except FileNotFoundError:
            print("未找到gemini命令，请确保已安装Google Cloud CLI")
            raise Exception("未找到gemini命令，请确保已安装Google Cloud CLI")
        except Exception as e:
            print(f"Gemini上下文合并失败: {e}")
            raise e 