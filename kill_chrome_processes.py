"""
This script is used to kill all Google Chrome processes running on the system.
"""
import os
import subprocess


def kill_chrome_processes():
    """
    Terminates all Google Chrome processes.
    """
    if os.name == 'nt':  # For Windows
        subprocess.call(["taskkill", "/F", "/IM", "chrome.exe", "/T"])
    else:  # For macOS and Linux
        subprocess.call(["pkill", "-f", "chrome"])


kill_chrome_processes()
