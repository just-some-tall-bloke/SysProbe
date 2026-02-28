import subprocess
import os
import warnings

# Suppress setuptools/distutils warnings from GPUtil
warnings.filterwarnings('ignore', category=DeprecationWarning)


class GPUCollector:
    @staticmethod
    def get_gpu_info():
        """Collect GPU information."""
        gpu_info = {}
        
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')
                import GPUtil
            gpus = GPUtil.getGPUs()
            if gpus:
                for i, gpu in enumerate(gpus):
                    prefix = f"GPU {i}" if len(gpus) > 1 else "GPU"
                    gpu_info[f"{prefix} - Name"] = gpu.name
                    gpu_info[f"{prefix} - Memory"] = f"{gpu.memoryTotal} MB"
                    gpu_info[f"{prefix} - Memory Free"] = f"{gpu.memoryFree} MB"
                    gpu_info[f"{prefix} - Memory Used"] = f"{gpu.memoryUsed} MB"
                    gpu_info[f"{prefix} - Load"] = f"{gpu.load * 100:.1f}%"
            else:
                gpu_info['GPU'] = 'No NVIDIA GPU detected'
        except Exception as e:
            gpu_info['Info'] = f"GPUtil unavailable: {str(e)}"
        
        # Try to get integrated graphics info
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            result = subprocess.run(
                ['powershell', '-NoProfile', '-Command', 'Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM | ConvertTo-Json'],
                capture_output=True,
                text=True,
                timeout=5,
                startupinfo=startupinfo
            )
            if result.returncode == 0 and result.stdout.strip():
                import json
                data = json.loads(result.stdout)
                
                # Convert to list if it's a single dict
                if isinstance(data, dict):
                    data = [data]
                    
                if isinstance(data, list):
                    for idx, item in enumerate(data):
                        name = item.get('Name', 'Unknown')
                        memory = item.get('AdapterRAM', 'Unknown')
                        if name and name != 'Unknown':
                            gpu_info[f"GPU {idx} - Name"] = name
                            if isinstance(memory, (int, float)):
                                gpu_info[f"GPU {idx} - Memory"] = f"{memory / (1024**3):.2f} GB"
                            elif isinstance(memory, str) and memory.isdigit():
                                gpu_info[f"GPU {idx} - Memory"] = f"{int(memory) / (1024**3):.2f} GB"
        except Exception as e:
            if 'GPU' not in gpu_info:
                gpu_info['Integrated GPU'] = f"Error: {str(e)}"
        
        return gpu_info if gpu_info else {'GPU': 'No GPU detected'}
