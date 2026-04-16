#!/usr/bin/env python3
"""
Build script to create standalone CppOS Launcher executable
This embeds the kernel binary into the launcher
"""

import os
import sys
import base64
import shutil
import subprocess

def embed_kernel():
    """Embed kernel binary into launcher script"""
    
    # Find kernel
    kernel_paths = [
        '../releases/cppos.bin',
        '../build/cppos.bin',
        '../../releases/cppos.bin',
        '../../build/cppos.bin',
    ]
    
    kernel_path = None
    for path in kernel_paths:
        if os.path.exists(path):
            kernel_path = path
            break
    
    if not kernel_path:
        print("ERROR: Kernel binary not found!")
        print("Please build the kernel first:")
        print("  cd .. && make")
        sys.exit(1)
    
    print(f"Found kernel: {kernel_path}")
    print(f"Size: {os.path.getsize(kernel_path)} bytes")
    
    # Read kernel
    with open(kernel_path, 'rb') as f:
        kernel_data = f.read()
    
    # Encode to base64
    kernel_b64 = base64.b64encode(kernel_data).decode('ascii')
    
    # Read launcher template
    with open('cppos_launcher.py', 'r') as f:
        launcher_code = f.read()
    
    # Replace placeholder with actual kernel data
    placeholder = 'CPPOS_KERNEL_BASE64 = """\n# Kernel binary will be embedded here during build process\n# For now, this looks for the external cppos.bin file\n"""'
    
    # Split base64 into lines of 80 chars
    b64_lines = [kernel_b64[i:i+80] for i in range(0, len(kernel_b64), 80)]
    b64_formatted = '\n'.join(b64_lines)
    
    new_kernel_var = f'CPPOS_KERNEL_BASE64 = """\n{b64_formatted}\n"""'
    
    launcher_code = launcher_code.replace(placeholder, new_kernel_var)
    
    # Write embedded launcher
    embedded_path = 'cppos_launcher_embedded.py'
    with open(embedded_path, 'w') as f:
        f.write(launcher_code)
    
    print(f"Created: {embedded_path}")
    return embedded_path

def build_executable():
    """Build standalone executable using PyInstaller"""
    
    # Check for PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
    
    # Embed kernel
    embedded_script = embed_kernel()
    
    # Build with PyInstaller
    print("\nBuilding executable...")
    
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name', 'CppOS',
        '--icon', 'NONE',
        '--clean',
        '--noconfirm',
        embedded_script
    ]
    
    subprocess.check_call(cmd)
    
    # Copy to releases
    exe_name = 'CppOS.exe' if sys.platform == 'win32' else 'CppOS'
    src = os.path.join('dist', exe_name)
    dst = os.path.join('..', 'releases', exe_name)
    
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"\n✅ Success! Executable created: {dst}")
        print(f"Size: {os.path.getsize(dst) / 1024:.1f} KB")
        print("\nThis executable includes the kernel and can run without external files!")
    else:
        print(f"\n❌ Error: Expected executable not found at {src}")

def build_simple():
    """Build without embedding - just package the launcher"""
    
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
    
    print("\nBuilding launcher (without embedded kernel)...")
    print("Kernel will be loaded from releases/cppos.bin")
    
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed',
        '--name', 'CppOS-Launcher',
        '--clean',
        '--noconfirm',
        'cppos_launcher.py'
    ]
    
    subprocess.check_call(cmd)
    
    exe_name = 'CppOS-Launcher.exe' if sys.platform == 'win32' else 'CppOS-Launcher'
    src = os.path.join('dist', exe_name)
    dst = os.path.join('..', 'releases', exe_name)
    
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"\n✅ Success! Launcher created: {dst}")
        print("\nNote: This launcher requires cppos.bin in the releases/ folder")

def main():
    print("CppOS Launcher Build Script")
    print("=" * 40)
    print()
    print("1. Build standalone executable (with embedded kernel)")
    print("2. Build launcher only (requires external kernel)")
    print("3. Just embed kernel (no executable build)")
    print()
    
    choice = input("Select option (1-3): ").strip()
    
    if choice == '1':
        build_executable()
    elif choice == '2':
        build_simple()
    elif choice == '3':
        embed_kernel()
    else:
        print("Invalid choice")

if __name__ == '__main__':
    main()
