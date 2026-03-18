#!/usr/bin/env python3
"""
SecOps: A system checking software.
 memory, disk, and network stats  and reports.
"""

import json
import platform
import socket
import sys
import time
from datetime import datetime
import psutil  

#Cpu info usage
def get_cpu_info():
    return {
        "percent": psutil.cpu_percent(interval=1),
        "count_logical": psutil.cpu_count(),
        "count_physical": psutil.cpu_count(logical=False),
        "freq_mhz": getattr(psutil.cpu_freq(), "current", None),
    }

#Ram info usage
def get_memory_info():
    mem = psutil.virtual_memory()
    return{
        "total_mb":round(mem.total /(1024 ** 2),1),
        "available_mb":round(mem.available / (1024 ** 2),1),
        "percent_used":mem.percent,
    }


#Monitors partition storage capacity.
def get_disk_info():
    disk = psutil.disk_usage("/")
    return {
        "total_gb":round(disk.total / (1024 ** 3), 2),
        "used_gb":round(disk.used / (1024 ** 3), 2),
        "free_gb":round(disk.free / (1024 ** 3), 2),
        "percent_used":disk.percent,
    }

#Retrieves active IPv4 network addresses.
def get_network_info():
    addrs = psutil.net_if_addrs()
    interfaces = {}
    for iface, addr_list in addrs.items():
        for addr in addr_list:
            # Keep only IPv4 addresses 
            if addr.family == socket.AF_INET:
                interfaces[iface] = addr.address
    return interfaces


#Collects OS and platform metadata.
def get_system_info():
    return{
        "hostname":socket.gethostname(),
        "platform":platform.platform(),
        "python_version":platform.python_version(),
        "boot_time":datetime.fromtimestamp(psutil.boot_time()).isoformat(),
    }

#Generates a JSON report and checks for resource thresholds.
def main():
    report={
        "timestamp":datetime.now().isoformat(),
        "system":get_system_info(),
        "cpu":get_cpu_info(),
        "memory":get_memory_info(),
        "disk":get_disk_info(),
        "network":get_network_info(),
    }
    # Print formatted JSON report to standard output
    print(json.dumps(report, indent=2))

    #RESUlT of the searching
    warnings = []
    if report["cpu"]["percent"] > 90:
        warnings.append("HIGH CPU usage")
    if report["memory"]["percent_used"] > 90:
        warnings.append("HIGH memory usage")
    if report["disk"]["percent_used"] > 90:
        warnings.append("LOW disk space")

    #Output status to standard error and set exit code
    if warnings:
        #Prints to stderr to avoid corrupting the JSON output
        print(f"\n WARNINGS: {', '.join(warnings)}", file=sys.stderr)
        return 1
    else:
        print("\ All Systems Has Been Checked [OK]",file=sys.stderr)
        return 0

if __name__ == "__main__":
    sys.exit(main())



'''INFO FOR THE CODE SOURCE of sec.py'''
'''psutil: Rodola, G. psutil (Python system and process utilities) https://psutil.readthedocs.io/
Python JSON Module: Python Software Foundation. json https://docs.python.org/3/library/json.html'''