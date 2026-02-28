# CPU-Z Clone - User Guide

## Getting Started

### Installation

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python main.py
   ```

## User Interface

### Main Window
The application displays system information across 6 tabs with a clean, professional interface:

```
┌─────────────────────────────────────────────┐
│  CPU-Z Clone - System Information      [_▢✕] │
├─────────────────────────────────────────────┤
│ System Information                          │
├─────────────────────────────────────────────┤
│  [💻CPU] [🧠Memory] [🎮Graphics] [🔧MB]... │
│                                             │
│ ┌─────────────────────────────────────────┐ │
│ │ CPU Information                         │ │
│ ├─────────────────────────────────────────┤ │
│ │ Model: 13th Gen Intel Core i7-13700KF  │ │
│ │ Architecture: X86_64                    │ │
│ │ Physical Cores: 16                      │ │
│ │ Logical Cores: 24                       │ │
│ │ Max Frequency: 3400.00 MHz              │ │
│ │ Current Frequency: 2400.00 MHz          │ │
│ │ ...                                     │ │
│ │                                         │ │
│ │                                         │ │
│ └─────────────────────────────────────────┘ │
│                                             │
│      [⏱️ Auto Refresh (OFF)] [🔄 Refresh]  │
└─────────────────────────────────────────────┘
```

### Tab Descriptions

#### 💻 CPU Tab
Displays processor information:
- Model name and brand
- Physical and logical core count
- Clock speeds (current, max)
- Cache sizes (L2, L3)
- Architecture
- Socket and package info

#### 🧠 Memory Tab
Shows RAM and swap memory:
- Total memory
- Used/Available memory
- Memory usage percentage
- Swap statistics
- Memory type (DDR4/DDR5)

#### 🎮 Graphics Tab
Graphics device information:
- NVIDIA GPU details (if present)
- GPU memory (VRAM)
- Memory usage
- Integrated graphics (if present)
- Driver information

#### 🔧 Motherboard Tab
Motherboard and BIOS info:
- Manufacturer
- Model
- BIOS version and date
- Chipset
- Serial number

#### 💾 Storage Tab
Storage devices and partitions:
- Drive letter/name
- File system type
- Total capacity
- Used/Free space
- Usage percentage

#### 🖥️ System Tab
Operating system information:
- OS name and version
- System architecture
- Hostname
- Uptime
- Boot time
- Python version

## Controls

### Refresh All Button
- **Action**: Manually update all system information
- **Speed**: Information is gathered in background threads, UI remains responsive
- **Frequency**: Click anytime to refresh

### Auto Refresh Toggle
- **OFF**: Manual refresh only
- **ON**: Automatically refresh all tabs every 5 seconds
- **Visual Indicator**: Button changes color (blue when OFF, green when ON)

## Features

✨ **Threading**: All data collection runs in background threads to keep UI responsive

🔄 **Auto-Refresh**: Optional automatic updates for real-time monitoring

📋 **Tabbed Interface**: Easy navigation between different system categories

🎨 **Professional Styling**: Modern Windows-style appearance

⚡ **Lightweight**: Minimal system resource usage

## Troubleshooting

### Missing Information
Some features require elevated (administrator) privileges:

```
Problem: Motherboard info shows "WMI Error"
Solution: Run the application as Administrator

Problem: Detailed RAM speed/type not showing
Solution: Run with admin privileges or check BIOS settings
```

### GPU Not Detected
- **NVIDIA**: Ensure graphics driver is installed
- **AMD**: May need additional setup (currently GPUtil supports NVIDIA)
- **Intel**: Integrated graphics detected via WMI

### Performance Issues
- The application is very lightweight
- If slow, check system resource usage
- Auto-refresh can be disabled if needed

## Building Standalone Executable

### Windows
```bash
build.bat
```

### Linux/Mac
```bash
bash build.sh
```

The executable will be created in `dist/CPU-Z-Clone.exe` (Windows).

## System Requirements

- **Python**: 3.8 or higher
- **OS**: Windows (primary), Linux/macOS with modifications
- **RAM**: Minimal (< 50 MB)
- **Disk Space**: ~200 MB (including dependencies)

## Common Questions

**Q: Can I minimize to system tray?**
A: Currently no, but this can be added as an enhancement

**Q: Does it work on Linux/Mac?**
A: Main code is cross-platform, but WMI (motherboard info) is Windows-only. Can be adapted.

**Q: Can I export the data?**
A: Not currently, but export to PDF/CSV can be added

**Q: Is admin required?**
A: No, but some features (BIOS info) work better with admin access

## License

MIT License - See LICENSE file for details

---

Enjoy using CPU-Z Clone! 🎉
