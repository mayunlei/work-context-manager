#!/usr/bin/env python3
"""
上下文切换器 - 主程序
通过语音记录和AI合并来管理项目上下文
"""

import threading
import time
from audio_recorder import AudioRecorder
from speech_recognition import SpeechRecognizer
from context_manager import ContextManager
from status_bar import StatusBarApp
from hotkey_manager import HotkeyManager
import config

class ContextSwitcher:
    def __init__(self):
        # 初始化各个模块
        self.audio_recorder = AudioRecorder(
            sample_rate=config.SAMPLE_RATE,
            channels=config.CHANNELS
        )
        self.speech_recognizer = SpeechRecognizer()
        self.context_manager = ContextManager()
        self.status_bar = StatusBarApp(on_backup=self.context_manager.backup_context)
        
        # 设置录音回调
        self.audio_recorder.on_recording_start = self._on_recording_start
        self.audio_recorder.on_recording_stop = self._on_recording_stop
        
        # 初始化快捷键管理器
        self.hotkey_manager = HotkeyManager(
            on_start_recording=self._start_recording,
            on_stop_recording=self._stop_recording
        )
        
        # 处理状态
        self.processing = False
    
    def start(self):
        """启动应用"""
        print("启动上下文切换器...")
        print(f"快捷键: {' + '.join(config.RECORD_HOTKEY)}")
        print(f"上下文文件: {config.CONTEXT_FILE}")
        print(f"历史记录文件: {config.HISTORY_FILE}")
        print(f"上下文合并: {config.CONTEXT_MERGE_PROVIDER} ({config.CONTEXT_MERGE_MODEL})")
        
        # 检查API配置
        if not config.OPENAI_API_KEY and not config.DASHSCOPE_API_KEY:
            print("警告: 未设置任何API密钥")
            self.status_bar.show_notification(
                "配置警告", 
                "未设置API密钥", 
                "请设置 OPENAI_API_KEY 或 DASHSCOPE_API_KEY 环境变量"
            )
        elif config.DASHSCOPE_API_KEY:
            print(f"使用DashScope API进行语音识别，模型: {config.DASHSCOPE_ASR_MODEL}")
        else:
            print("使用OpenAI API进行语音识别")
        
        # 启动快捷键监听
        self.hotkey_manager.start_listening()
        
        # 启动状态栏
        self.status_bar.run()
    
    def _start_recording(self):
        """开始录音"""
        if self.processing:
            return
            
        self.audio_recorder.start_recording()
        self.status_bar.set_recording_state(True)
        self.status_bar.show_notification(
            "录音开始", 
            "正在录音...", 
            "松开快捷键停止录音"
        )
    
    def _stop_recording(self):
        """停止录音"""
        if not self.audio_recorder.is_recording():
            return
            
        self.status_bar.set_recording_state(False)
        self.status_bar.show_notification(
            "录音结束", 
            "正在处理...", 
            "请稍候"
        )
        
        # 在后台线程中处理录音
        threading.Thread(target=self._process_recording).start()
    
    def _process_recording(self):
        """处理录音"""
        self.processing = True
        
        try:
            # 停止录音并获取音频数据
            audio_data = self.audio_recorder.stop_recording()
            if not audio_data:
                self.status_bar.show_notification(
                    "处理失败", 
                    "未获取到音频数据", 
                    "请重试"
                )
                return
            
            # 语音识别
            self.status_bar.show_notification(
                "正在识别", 
                "语音转文字中...", 
                "请稍候"
            )
            
            transcribed_text = self.speech_recognizer.transcribe_audio(audio_data)
            if not transcribed_text:
                self.status_bar.show_notification(
                    "识别失败", 
                    "语音识别失败", 
                    "请检查网络和API配置"
                )
                return
            
            # 读取现有上下文
            existing_context = self.context_manager.read_context()
            
            # 合并上下文
            self.status_bar.show_notification(
                "正在合并", 
                "合并上下文中...", 
                "请稍候"
            )
            
            merged_context = self.speech_recognizer.merge_context(
                existing_context, 
                transcribed_text
            )
            
            # 保存新上下文
            self.context_manager.write_context(merged_context)
            
            # 添加历史记录
            self.context_manager.add_history(
                existing_context,
                transcribed_text,
                merged_context
            )
            
            # 显示成功通知
            self.status_bar.show_notification(
                "处理完成", 
                "上下文已更新", 
                f"识别内容: {transcribed_text[:50]}..."
            )
            
        except Exception as e:
            print(f"处理录音时出错: {e}")
            self.status_bar.show_notification(
                "处理失败", 
                "发生错误", 
                str(e)
            )
        finally:
            self.processing = False
    
    def _on_recording_start(self):
        """录音开始回调"""
        self.status_bar.set_recording_state(True)
    
    def _on_recording_stop(self):
        """录音停止回调"""
        self.status_bar.set_recording_state(False)

def main():
    """主函数"""
    app = ContextSwitcher()
    app.start()

if __name__ == "__main__":
    main() 