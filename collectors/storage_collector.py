import psutil


class StorageCollector:
    @staticmethod
    def get_storage_info():
        """Collect storage and partition information."""
        storage_info = {}
        
        try:
            partitions = psutil.disk_partitions()
            for idx, partition in enumerate(partitions):
                prefix = f"Drive {chr(65 + idx)}" if partition.device else f"Partition {idx}"
                
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    storage_info[f"{prefix} - Device"] = partition.device
                    storage_info[f"{prefix} - Mount Point"] = partition.mountpoint
                    storage_info[f"{prefix} - File System"] = partition.fstype
                    storage_info[f"{prefix} - Total"] = f"{usage.total / (1024**3):.2f} GB"
                    storage_info[f"{prefix} - Used"] = f"{usage.used / (1024**3):.2f} GB"
                    storage_info[f"{prefix} - Free"] = f"{usage.free / (1024**3):.2f} GB"
                    storage_info[f"{prefix} - Usage %"] = f"{usage.percent}%"
                except PermissionError:
                    storage_info[f"{prefix} - Status"] = "Permission denied"
                except Exception as e:
                    storage_info[f"{prefix} - Error"] = str(e)
        except Exception as e:
            storage_info['Error'] = str(e)
        
        return storage_info if storage_info else {'Storage': 'No info available'}
