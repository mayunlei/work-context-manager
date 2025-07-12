import os
from datetime import datetime
from pathlib import Path
import config

class ContextManager:
    def __init__(self):
        self.context_file = config.CONTEXT_FILE
        self.history_file = config.HISTORY_FILE
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """确保文件存在"""
        # 确保桌面目录存在
        config.DESKTOP_PATH.mkdir(exist_ok=True)
        
        # 创建上下文文件
        if not self.context_file.exists():
            self.context_file.write_text("# 上下文切换器\n\n## 使用说明\n\n- 按住 Cmd+Shift+D 开始录音\n- 松开按键停止录音并处理\n- 语音内容将自动合并到上下文中\n\n", encoding='utf-8')
        
        # 创建历史记录文件
        if not self.history_file.exists():
            self.history_file.write_text("# 上下文切换器 - 历史记录\n\n", encoding='utf-8')
    
    def read_context(self) -> str:
        """读取当前上下文"""
        try:
            return self.context_file.read_text(encoding='utf-8')
        except Exception as e:
            print(f"读取上下文文件失败: {e}")
            return ""
    
    def write_context(self, content: str):
        """写入上下文"""
        try:
            self.context_file.write_text(content, encoding='utf-8')
        except Exception as e:
            print(f"写入上下文文件失败: {e}")
    
    def add_history(self, original_content: str, new_content: str, merged_content: str):
        """添加历史记录"""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            history_entry = f"""
## {timestamp}

### 原始内容
{original_content}

### 新内容
{new_content}

### 合并后内容
{merged_content}

---
"""
            
            # 追加到历史文件
            with open(self.history_file, 'a', encoding='utf-8') as f:
                f.write(history_entry)
                
        except Exception as e:
            print(f"写入历史记录失败: {e}")
    
    def backup_context(self):
        """备份当前上下文"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = config.DESKTOP_PATH / f"context_backup_{timestamp}.md"
            current_content = self.read_context()
            backup_file.write_text(current_content, encoding='utf-8')
            print(f"上下文已备份到: {backup_file}")
        except Exception as e:
            print(f"备份失败: {e}") 