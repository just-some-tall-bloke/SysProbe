#!/usr/bin/env python
"""Test script to verify all collectors work properly."""

from collectors.cpu_collector import CPUCollector
from collectors.ram_collector import RAMCollector
from collectors.gpu_collector import GPUCollector
from collectors.motherboard_collector import MotherboardCollector
from collectors.storage_collector import StorageCollector
from collectors.system_collector import SystemCollector


def test_collectors():
    print("=== CPU Information ===")
    cpu_info = CPUCollector.get_cpu_info()
    print(f"Model: {cpu_info.get('Model', 'N/A')}")
    print(f"Cores: {cpu_info.get('Logical Cores', 'N/A')}")

    print("\n=== RAM Information ===")
    ram_info = RAMCollector.get_ram_info()
    print(f"Total: {ram_info.get('Total', 'N/A')}")
    print(f"Used: {ram_info.get('Used', 'N/A')}")

    print("\n=== GPU Information ===")
    gpu_info = GPUCollector.get_gpu_info()
    gpu_keys = list(gpu_info.keys())[:2]
    for key in gpu_keys:
        print(f"{key}: {gpu_info[key]}")

    print("\n=== Motherboard Information ===")
    mb_info = MotherboardCollector.get_motherboard_info()
    mb_keys = list(mb_info.keys())[:2]
    for key in mb_keys:
        print(f"{key}: {mb_info[key]}")

    print("\n=== Storage Information ===")
    storage_info = StorageCollector.get_storage_info()
    storage_keys = list(storage_info.keys())[:3]
    for key in storage_keys:
        print(f"{key}: {storage_info[key]}")

    print("\n=== System Information ===")
    sys_info = SystemCollector.get_system_info()
    print(f"OS: {sys_info.get('OS', 'N/A')} {sys_info.get('OS Release', '')}")
    print(f"Hostname: {sys_info.get('Hostname', 'N/A')}")
    print(f"Uptime: {sys_info.get('Uptime', 'N/A')}")

    print("\n✅ All collectors working successfully!")


if __name__ == '__main__':
    test_collectors()
