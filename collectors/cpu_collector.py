import cpuinfo
import psutil


class CPUCollector:
    @staticmethod
    def get_cpu_info():
        """Collect detailed CPU information."""
        try:
            info = cpuinfo.get_cpu_info()
            cpu_count_phys = psutil.cpu_count(logical=False) or 1
            cpu_count_logical = psutil.cpu_count(logical=True)
            
            return {
                'Model': info.get('brand_raw', 'Unknown'),
                'Architecture': info.get('arch', 'Unknown'),
                'Physical Cores': str(cpu_count_phys),
                'Logical Cores': str(cpu_count_logical),
                'Max Frequency': f"{psutil.cpu_freq().max:.2f} MHz" if psutil.cpu_freq() else 'Unknown',
                'Current Frequency': f"{psutil.cpu_freq().current:.2f} MHz" if psutil.cpu_freq() else 'Unknown',
                'Bus Speed': info.get('hz_advertised_raw', ['Unknown'])[0] if info.get('hz_advertised_raw') else 'Unknown',
                'L2 Cache': info.get('l2_cache_size', 'Unknown'),
                'L3 Cache': info.get('l3_cache_size', 'Unknown'),
                'Socket': info.get('l2_cache_per_core', 'Unknown'),
                'Package': 'Single' if cpu_count_phys == psutil.cpu_count(logical=True) / 2 else 'Multiple',
                'Technology': info.get('stepping', 'Unknown'),
                'TDP': 'Unknown',
            }
        except Exception as e:
            return {'Error': str(e)}
