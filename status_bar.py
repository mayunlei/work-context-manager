import rumps
import threading
from typing import Callable

class StatusBarApp(rumps.App):
    def __init__(self, on_backup: Callable = None):
        super().__init__("🎤", quit_button=None)
        self.on_backup = on_backup
        self.is_recording = False
        self._setup_menu()
    
    def _setup_menu(self):
        """设置菜单"""
        self.menu = [
            rumps.MenuItem("备份上下文", callback=self._backup_context),
            rumps.MenuItem("打开上下文文件", callback=self._open_context_file),
            rumps.MenuItem("打开历史记录", callback=self._open_history_file),
            None,  # 分隔线
            rumps.MenuItem("退出", callback=self._quit_app)
        ]
    
    def set_recording_state(self, recording: bool):
        """设置录音状态"""
        self.is_recording = recording
        if recording:
            self.title = "🔴"  # 红色表示正在录音
        else:
            self.title = "🎤"  # 黑色表示未录音
    
    def _backup_context(self, _):
        """备份上下文"""
        if self.on_backup:
            self.on_backup()
        else:
            rumps.notification("上下文切换器", "备份", "备份功能未配置")
    
    def _open_context_file(self, _):
        """打开上下文文件"""
        import subprocess
        import config
        try:
            subprocess.run(["open", str(config.CONTEXT_FILE)])
        except Exception as e:
            rumps.notification("错误", "打开文件失败", str(e))
    
    def _open_history_file(self, _):
        """打开历史记录文件"""
        import subprocess
        import config
        try:
            subprocess.run(["open", str(config.HISTORY_FILE)])
        except Exception as e:
            rumps.notification("错误", "打开文件失败", str(e))
    
    def _quit_app(self, _):
        """退出应用"""
        rumps.quit_application()
    
    def show_notification(self, title: str, subtitle: str, message: str):
        """显示通知"""
        rumps.notification(title, subtitle, message) 