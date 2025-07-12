import sounddevice as sd
import numpy as np
import threading
import time
from typing import Optional, Callable
import io
import wave

class AudioRecorder:
    def __init__(self, sample_rate=16000, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.audio_data = []
        self.recording_thread = None
        self.on_recording_start: Optional[Callable] = None
        self.on_recording_stop: Optional[Callable] = None
        
    def start_recording(self):
        """开始录音"""
        if self.recording:
            return
            
        self.recording = True
        self.audio_data = []
        
        if self.on_recording_start:
            self.on_recording_start()
            
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.recording_thread.start()
        
    def stop_recording(self):
        """停止录音"""
        if not self.recording:
            return None
            
        self.recording = False
        
        if self.recording_thread:
            self.recording_thread.join()
            
        if self.on_recording_stop:
            self.on_recording_stop()
            
        return self._save_audio()
    
    def _record_audio(self):
        """录音线程"""
        def callback(indata, frames, time, status):
            if self.recording:
                self.audio_data.append(indata.copy())
        
        with sd.InputStream(callback=callback,
                          channels=self.channels,
                          samplerate=self.sample_rate,
                          dtype=np.int16):
            while self.recording:
                time.sleep(0.1)
    
    def _save_audio(self) -> Optional[bytes]:
        """保存录音为WAV格式的字节数据"""
        if not self.audio_data:
            return None
            
        # 合并所有音频数据
        audio_array = np.concatenate(self.audio_data, axis=0)
        
        # 创建WAV文件
        buffer = io.BytesIO()
        with wave.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_array.tobytes())
        
        return buffer.getvalue()
    
    def is_recording(self) -> bool:
        """检查是否正在录音"""
        return self.recording 