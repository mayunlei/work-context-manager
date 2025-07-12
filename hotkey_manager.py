from pynput import keyboard
from typing import Callable
import config

class HotkeyManager:
    def __init__(self, on_start_recording: Callable, on_stop_recording: Callable):
        self.on_start_recording = on_start_recording
        self.on_stop_recording = on_stop_recording
        self.pressed_keys = set()
        self.recording = False
        self.listener = None
    
    def start_listening(self):
        """开始监听快捷键"""
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.start()
    
    def stop_listening(self):
        """停止监听快捷键"""
        if self.listener:
            self.listener.stop()
    
    def _on_press(self, key):
        """按键按下事件"""
        try:
            # 获取按键名称
            if hasattr(key, 'char'):
                key_name = key.char.lower()
            else:
                key_name = str(key).replace('Key.', '').lower()
            
            self.pressed_keys.add(key_name)
            
            # 检查是否按下目标组合键
            if self._is_target_hotkey_pressed() and not self.recording:
                self.recording = True
                if self.on_start_recording:
                    self.on_start_recording()
                    
        except Exception as e:
            print(f"按键处理错误: {e}")
    
    def _on_release(self, key):
        """按键释放事件"""
        try:
            # 获取按键名称
            if hasattr(key, 'char'):
                key_name = key.char.lower()
            else:
                key_name = str(key).replace('Key.', '').lower()
            
            # 从已按下的键集合中移除
            self.pressed_keys.discard(key_name)
            
            # 检查是否释放了目标组合键
            if not self._is_target_hotkey_pressed() and self.recording:
                self.recording = False
                if self.on_stop_recording:
                    self.on_stop_recording()
                    
        except Exception as e:
            print(f"按键释放处理错误: {e}")
    
    def _is_target_hotkey_pressed(self) -> bool:
        """检查目标快捷键是否被按下"""
        target_keys = config.RECORD_HOTKEY
        return all(key in self.pressed_keys for key in target_keys) 