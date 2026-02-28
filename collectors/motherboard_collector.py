import subprocess
import os


class MotherboardCollector:
    @staticmethod
    def get_motherboard_info():
        """Collect motherboard information using Windows WMI."""
        mb_info = {}
        
        try:
            # Get motherboard info
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            result = subprocess.run(
                ['powershell', '-NoProfile', '-Command', 'Get-CimInstance Win32_BaseBoard | Select-Object Manufacturer, Product, Version, SerialNumber | ConvertTo-Json'],
                capture_output=True,
                text=True,
                timeout=5,
                startupinfo=startupinfo
            )
            if result.returncode == 0 and result.stdout.strip():
                import json
                data = json.loads(result.stdout)
                mb_info['Manufacturer'] = data.get('Manufacturer', 'Unknown')
                mb_info['Model'] = data.get('Product', 'Unknown')
                mb_info['Version'] = data.get('Version', 'Unknown')
                mb_info['Serial Number'] = data.get('SerialNumber', 'Unknown')
        except Exception as e:
            mb_info['Motherboard Error'] = str(e)
        
        # Get BIOS info
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            result = subprocess.run(
                ['powershell', '-NoProfile', '-Command', 'Get-CimInstance Win32_BIOS | Select-Object Manufacturer, SMBIOSBIOSVersion, ReleaseDate | ConvertTo-Json'],
                capture_output=True,
                text=True,
                timeout=5,
                startupinfo=startupinfo
            )
            if result.returncode == 0 and result.stdout.strip():
                import json
                data = json.loads(result.stdout)
                mb_info['BIOS Manufacturer'] = data.get('Manufacturer', 'Unknown')
                mb_info['BIOS Version'] = data.get('SMBIOSBIOSVersion', 'Unknown')
                
                # Release date might need formatting, but we'll try to get it straight first
                date_val = data.get('ReleaseDate')
                if date_val:
                    if isinstance(date_val, str) and date_val.startswith('/Date('):
                        # Handle powershell JSON date format /Date(ms)/
                        import re
                        match = re.search(r'\\/Date\((\d+)\)\\/', date_val)
                        if match:
                            import datetime
                            mb_info['BIOS Release Date'] = datetime.datetime.fromtimestamp(int(match.group(1))/1000.0).strftime('%Y-%m-%d')
                        else:
                            mb_info['BIOS Release Date'] = date_val
                    else:
                        mb_info['BIOS Release Date'] = str(date_val)
                else:
                    mb_info['BIOS Release Date'] = 'Unknown'
        except Exception as e:
            mb_info['BIOS Error'] = str(e)
        
        # Get chipset info
        try:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            
            result = subprocess.run(
                ['powershell', '-NoProfile', '-Command', 'Get-CimInstance Win32_IDEController -ErrorAction SilentlyContinue | Select-Object Name | ConvertTo-Json'],
                capture_output=True,
                text=True,
                timeout=5,
                startupinfo=startupinfo
            )
            if result.returncode == 0 and result.stdout.strip():
                import json
                data = json.loads(result.stdout)
                if isinstance(data, list) and len(data) > 0:
                    mb_info['Chipset'] = data[0].get('Name', 'Unknown')
                elif isinstance(data, dict):
                    mb_info['Chipset'] = data.get('Name', 'Unknown')
        except Exception as e:
            mb_info['Chipset Error'] = str(e)
        
        return mb_info if mb_info else {'Motherboard': 'No info available'}
