#!/usr/bin/env python
"""
Launcher script for QR Code Generator Application
"""

import sys
import os
import subprocess
import importlib.util

def check_dependencies():
    """Check if required packages are installed."""
    required_packages = ['qrcode', 'pillow']
    missing_packages = []
    
    for package in required_packages:
        if package == 'pillow':
            # Pillow is imported as PIL
            package_name = 'PIL'
        else:
            package_name = package
            
        spec = importlib.util.find_spec(package_name)
        if spec is None:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:", ", ".join(missing_packages))
        install = input("Would you like to install them now? (y/n): ")
        if install.lower() == 'y':
            for package in missing_packages:
                print(f"Installing {package}...")
                try:
                    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                except subprocess.CalledProcessError:
                    print(f"Failed to install {package}. Please install it manually.")
                    sys.exit(1)
        else:
            print("Please install the required packages and try again.")
            sys.exit(1)

def main():
    """Main function to launch the application."""
    check_dependencies()
    
    # Import the main application module
    try:
        from qr_code_generator import QRCodeGenerator
    except ImportError:
        print("Could not find qr_code_generator.py in the current directory.")
        sys.exit(1)
    
    import tkinter as tk
    root = tk.Tk()
    app = QRCodeGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()