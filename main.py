import sys
import threading
import os
import tempfile
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QPushButton, QTextEdit, QLabel, QHBoxLayout, QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QTimer
from PyQt5.QtGui import QFont, QColor, QTextCursor

from collectors.cpu_collector import CPUCollector
from collectors.ram_collector import RAMCollector
from collectors.gpu_collector import GPUCollector
from collectors.motherboard_collector import MotherboardCollector
from collectors.storage_collector import StorageCollector
from collectors.system_collector import SystemCollector




class SingleInstanceLock:
    def __init__(self, app_name="SysProbe"):
        self.lock_file = os.path.join(tempfile.gettempdir(), f"{app_name}.lock")
        self.lock = None
        self.is_windows = sys.platform == 'win32'
    
    def acquire(self):
        try:
            self.lock = open(self.lock_file, 'w')
            
            if self.is_windows:
                import msvcrt
                msvcrt.locking(self.lock.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(self.lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            
            return True
        except (OSError, IOError, BlockingIOError):
            if self.lock:
                self.lock.close()
                self.lock = None
            return False
    
    def release(self):
        if self.lock:
            try:
                if self.is_windows:
                    import msvcrt
                    msvcrt.locking(self.lock.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl
                    fcntl.flock(self.lock.fileno(), fcntl.LOCK_UN)
                
                self.lock.close()
                os.remove(self.lock_file)
            except:
                pass


class InfoUpdater(QObject):
    update_signal = pyqtSignal(str, str)

    def update_info(self, tab_name, collector_func):
        try:
            info = collector_func()
            text = self._format_info(info)
            self.update_signal.emit(tab_name, text)
        except Exception as e:
            self.update_signal.emit(tab_name, f"Error: {str(e)}")

    @staticmethod
    def _format_info(info_dict):
        if isinstance(info_dict, dict):
            return '\n'.join([f"{k}: {v}" for k, v in info_dict.items()])
        return str(info_dict)


class CPUZClone(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SysProbe - System Information')
        self.setGeometry(100, 100, 1000, 750)
        self.setMinimumSize(900, 650)
        
        self.updater = InfoUpdater()
        self.updater.update_signal.connect(self.on_info_updated)
        
        self.tab_displays = {}
        
        # Auto-refresh timer (every 5 seconds)
        self.auto_refresh_timer = QTimer()
        self.auto_refresh_timer.timeout.connect(self.refresh_all_info)
        self.auto_refresh_enabled = False
        
        self.init_ui()
        self.refresh_all_info()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Title bar
        title_layout = QHBoxLayout()
        title_label = QLabel('System Information')
        title_font = QFont('Arial', 14, QFont.Bold)
        title_label.setFont(title_font)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        tabs = QTabWidget()
        self.tabs = tabs
        
        self.tab_displays['CPU'] = self.create_info_tab('CPU Information')
        self.tab_displays['RAM'] = self.create_info_tab('Memory Information')
        self.tab_displays['GPU'] = self.create_info_tab('Graphics Information')
        self.tab_displays['Motherboard'] = self.create_info_tab('Motherboard Information')
        self.tab_displays['Storage'] = self.create_info_tab('Storage Information')
        self.tab_displays['System'] = self.create_info_tab('System Information')
        
        tabs.addTab(self.tab_displays['CPU']['widget'], '💻 CPU')
        tabs.addTab(self.tab_displays['RAM']['widget'], '🧠 Memory')
        tabs.addTab(self.tab_displays['GPU']['widget'], '🎮 Graphics')
        tabs.addTab(self.tab_displays['Motherboard']['widget'], '🔧 Motherboard')
        tabs.addTab(self.tab_displays['Storage']['widget'], '💾 Storage')
        tabs.addTab(self.tab_displays['System']['widget'], '🖥️ System')
        
        layout.addWidget(tabs)
        
        button_layout = QHBoxLayout()
        refresh_btn = QPushButton('🔄 Refresh All')
        refresh_btn.clicked.connect(self.refresh_all_info)
        
        auto_refresh_btn = QPushButton('⏱️ Auto Refresh (OFF)')
        auto_refresh_btn.clicked.connect(self.toggle_auto_refresh)
        auto_refresh_btn.setMinimumWidth(150)
        self.auto_refresh_btn = auto_refresh_btn
        
        button_layout.addStretch()
        button_layout.addWidget(auto_refresh_btn)
        button_layout.addWidget(refresh_btn)
        
        layout.addLayout(button_layout)
        central_widget.setLayout(layout)
        
        # Apply stylesheet
        self.apply_stylesheet()

    def apply_stylesheet(self):
        style = """
        QMainWindow {
            background-color: #f5f5f5;
        }
        QTabWidget::pane {
            border: 1px solid #ddd;
        }
        QTabBar::tab {
            background-color: #e0e0e0;
            padding: 8px 20px;
            margin-right: 2px;
        }
        QTabBar::tab:selected {
            background-color: #ffffff;
            border-bottom: 3px solid #0078d4;
        }
        QPushButton {
            background-color: #0078d4;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #106ebe;
        }
        QPushButton:pressed {
            background-color: #0d47a1;
        }
        QTextEdit {
            background-color: #ffffff;
            border: 1px solid #ddd;
            padding: 10px;
        }
        """
        self.setStyleSheet(style)

    def create_info_tab(self, title):
        widget = QWidget()
        layout = QVBoxLayout()
        
        label = QLabel(title)
        label.setFont(QFont('Arial', 11, QFont.Bold))
        label.setStyleSheet("color: #333333; padding: 5px;")
        
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setFont(QFont('Consolas', 10))
        
        layout.addWidget(label)
        layout.addWidget(text_edit)
        layout.setContentsMargins(10, 10, 10, 10)
        
        widget.setLayout(layout)
        return {'widget': widget, 'text_edit': text_edit, 'label': label}

    def toggle_auto_refresh(self):
        self.auto_refresh_enabled = not self.auto_refresh_enabled
        if self.auto_refresh_enabled:
            self.auto_refresh_timer.start(5000)
            self.auto_refresh_btn.setText('⏱️ Auto Refresh (ON)')
            self.auto_refresh_btn.setStyleSheet("background-color: #107c10;")
        else:
            self.auto_refresh_timer.stop()
            self.auto_refresh_btn.setText('⏱️ Auto Refresh (OFF)')
            self.auto_refresh_btn.setStyleSheet("")

    def refresh_all_info(self):
        self.refresh_tab('CPU', CPUCollector.get_cpu_info)
        self.refresh_tab('RAM', RAMCollector.get_ram_info)
        self.refresh_tab('GPU', GPUCollector.get_gpu_info)
        self.refresh_tab('Motherboard', MotherboardCollector.get_motherboard_info)
        self.refresh_tab('Storage', StorageCollector.get_storage_info)
        self.refresh_tab('System', SystemCollector.get_system_info)

    def refresh_tab(self, tab_name, collector_func):
        thread = threading.Thread(target=self.updater.update_info, args=(tab_name, collector_func))
        thread.daemon = True
        thread.start()

    def on_info_updated(self, tab_name, text):
        if tab_name in self.tab_displays:
            self.tab_displays[tab_name]['text_edit'].setText(text)


def main():
    lock = SingleInstanceLock()
    if not lock.acquire():
        print("SysProbe is already running!")
        sys.exit(1)
    
    try:
        app = QApplication(sys.argv)
        window = CPUZClone()
        window.show()
        sys.exit(app.exec_())
    finally:
        lock.release()


if __name__ == '__main__':
    main()
