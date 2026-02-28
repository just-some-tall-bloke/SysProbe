# CPU-Z Clone

A Python-based system information utility that displays detailed hardware and system information similar to CPU-Z.

## Features

- **CPU Information**: Processor model, cores, threads, clock speeds, cache levels
- **Memory Information**: RAM stats, swap memory, usage percentages
- **Graphics Information**: GPU details, VRAM, integrated graphics info
- **Motherboard Information**: Manufacturer, model, BIOS version, chipset
- **Storage Information**: Drive details, partitions, capacity, usage
- **System Information**: OS, uptime, hostname, architecture

## Requirements

- Python 3.8+
- Windows (or Linux/macOS with modifications)

## Installation

1. Clone or download this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

The GUI will display system information in multiple tabs. Use the "Refresh All" button to update the information.

## Building Executable

To create a standalone `.exe` file:

```bash
pyinstaller --onefile --windowed --icon=icon.ico --name=CPU-Z-Clone main.py
```

The executable will be in the `dist/` folder.

## Project Structure

```
CPU-Specs/
├── main.py                          # Main GUI application
├── requirements.txt                 # Python dependencies
├── collectors/
│   ├── __init__.py
│   ├── cpu_collector.py            # CPU information
│   ├── ram_collector.py            # Memory information
│   ├── gpu_collector.py            # GPU information
│   ├── motherboard_collector.py     # Motherboard information
│   ├── storage_collector.py         # Storage information
│   └── system_collector.py          # System information
└── README.md
```

## Notes

- Some features (detailed motherboard BIOS info, detailed RAM specs) may require administrator privileges
- GPU detection works best with NVIDIA GPUs; integrated GPUs are detected via WMI
- The application uses threading to prevent UI freezing during information gathering

## License

MIT
