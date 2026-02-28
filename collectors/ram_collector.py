import psutil


class RAMCollector:
    @staticmethod
    def get_ram_info():
        """Collect detailed RAM information."""
        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                'Total': f"{mem.total / (1024**3):.2f} GB",
                'Available': f"{mem.available / (1024**3):.2f} GB",
                'Used': f"{mem.used / (1024**3):.2f} GB",
                'Free': f"{mem.free / (1024**3):.2f} GB",
                'Usage': f"{mem.percent}%",
                'Swap Total': f"{swap.total / (1024**3):.2f} GB",
                'Swap Used': f"{swap.used / (1024**3):.2f} GB",
                'Swap Free': f"{swap.free / (1024**3):.2f} GB",
                'Swap Usage': f"{swap.percent}%",
                'Type': 'DDR4/DDR5 (Auto-detect)',
                'Speed': 'Requires admin access',
                'Modules': 'Detailed info requires WMI access',
            }
        except Exception as e:
            return {'Error': str(e)}
