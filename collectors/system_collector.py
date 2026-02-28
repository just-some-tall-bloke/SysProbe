import platform
import psutil
import socket
from datetime import datetime, timedelta


class SystemCollector:
    @staticmethod
    def get_system_info():
        """Collect system and OS information."""
        try:
            boot_time = datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.now() - boot_time
            
            return {
                'OS': platform.system(),
                'OS Release': platform.release(),
                'OS Version': platform.version(),
                'Architecture': platform.architecture()[0],
                'Hostname': socket.gethostname(),
                'Processor': platform.processor(),
                'Python Version': platform.python_version(),
                'Boot Time': boot_time.strftime('%Y-%m-%d %H:%M:%S'),
                'Uptime': str(uptime).split('.')[0],
                'CPU Count (Logical)': str(psutil.cpu_count(logical=True)),
                'CPU Count (Physical)': str(psutil.cpu_count(logical=False) or 1),
            }
        except Exception as e:
            return {'Error': str(e)}
