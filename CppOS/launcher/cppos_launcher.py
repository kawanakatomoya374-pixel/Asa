#!/usr/bin/env python3
"""
CppOS Launcher - GUI Application to run CppOS with QEMU
"""

import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import platform
import tempfile
import shutil

# Embedded CppOS kernel binary (base64 encoded)
# This is a placeholder - the real binary will be embedded during build
CPPOS_KERNEL_BASE64 = """
# Kernel binary will be embedded here during build process
# For now, this looks for the external cppos.bin file
"""

class CppOSLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("CppOS Launcher")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Platform detection
        self.platform = platform.system()
        self.qemu_path = None
        self.kernel_path = None
        
        self.setup_ui()
        self.find_qemu()
        self.extract_kernel()
        
    def setup_ui(self):
        """Setup the GUI"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="🖥️ CppOS Launcher",
            font=('Helvetica', 20, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Description
        desc_label = ttk.Label(
            main_frame,
            text="C++ Operating System - Run CppOS instantly with QEMU",
            font=('Helvetica', 10)
        )
        desc_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.qemu_status = ttk.Label(status_frame, text="🔍 QEMU: Searching...", foreground="orange")
        self.qemu_status.grid(row=0, column=0, sticky=tk.W)
        
        self.kernel_status = ttk.Label(status_frame, text="🔍 Kernel: Searching...", foreground="orange")
        self.kernel_status.grid(row=1, column=0, sticky=tk.W)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        self.run_button = ttk.Button(
            button_frame,
            text="▶️ Run CppOS",
            command=self.run_os,
            state=tk.DISABLED
        )
        self.run_button.grid(row=0, column=0, padx=5)
        
        ttk.Button(
            button_frame,
            text="🛑 Stop",
            command=self.stop_os
        ).grid(row=0, column=1, padx=5)
        
        ttk.Button(
            button_frame,
            text="ℹ️ About",
            command=self.show_about
        ).grid(row=0, column=2, padx=5)
        
        # Console output
        console_frame = ttk.LabelFrame(main_frame, text="Console Output", padding="5")
        console_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.console = scrolledtext.ScrolledText(
            console_frame,
            width=70,
            height=10,
            state=tk.DISABLED,
            bg='black',
            fg='lightgreen',
            font=('Consolas', 9)
        )
        self.console.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        self.process = None
        
    def log(self, message):
        """Add message to console"""
        self.console.config(state=tk.NORMAL)
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)
        self.console.config(state=tk.DISABLED)
        
    def find_qemu(self):
        """Find QEMU installation"""
        self.log(f"Platform detected: {self.platform}")
        self.log("Searching for QEMU...")
        
        qemu_names = ['qemu-system-i386', 'qemu-system-i386.exe', 'qemu', 'qemu.exe']
        
        # Check in PATH
        self.log("Checking PATH...")
        for name in qemu_names:
            qemu_path = shutil.which(name)
            if qemu_path:
                self.qemu_path = qemu_path
                self.qemu_status.config(text=f"✅ QEMU: {qemu_path}", foreground="green")
                self.log(f"✓ Found QEMU in PATH: {qemu_path}")
                self.update_run_button()
                return
        
        # Check common locations on Windows
        if self.platform == 'Windows':
            self.log("Checking common Windows locations...")
            common_paths = [
                r"C:\Program Files\qemu\qemu-system-i386.exe",
                r"C:\Program Files (x86)\qemu\qemu-system-i386.exe",
                r"C:\qemu\qemu-system-i386.exe",
                r"C:\msys64\mingw64\bin\qemu-system-i386.exe",
                r"C:\msys64\mingw32\bin\qemu-system-i386.exe",
                r"C:\msys64\usr\bin\qemu-system-i386.exe",
            ]
            for path in common_paths:
                self.log(f"  Checking: {path}")
                if os.path.exists(path):
                    self.qemu_path = path
                    self.qemu_status.config(text=f"✅ QEMU: {path}", foreground="green")
                    self.log(f"✓ Found QEMU: {path}")
                    self.update_run_button()
                    return
        
        self.qemu_status.config(text="❌ QEMU: Not found", foreground="red")
        self.log("✗ ERROR: QEMU not found!")
        self.log("")
        self.log("QEMU is required to run CppOS.")
        self.log("Installation options:")
        self.log("  Windows: https://qemu.weilnetz.de/w64/")
        self.log("  MSYS2: pacman -S qemu")
        self.log("  Ubuntu/Debian: sudo apt-get install qemu-system-x86")
        self.log("")
        self.log("After installation, make sure qemu-system-i386 is in your PATH.")
        
    def extract_kernel(self):
        """Extract or find kernel binary"""
        self.log("Searching for kernel...")
        
        # Get the launcher directory and project root
        launcher_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(launcher_dir)
        current_dir = os.getcwd()
        
        self.log(f"Launcher dir: {launcher_dir}")
        self.log(f"Project root: {project_root}")
        self.log(f"Current dir: {current_dir}")
        
        # Try multiple possible locations
        possible_paths = [
            # From project root (most common)
            os.path.join(project_root, 'releases', 'cppos.bin'),
            os.path.join(project_root, 'build', 'cppos.bin'),
            # From current directory
            os.path.join(current_dir, 'releases', 'cppos.bin'),
            os.path.join(current_dir, 'build', 'cppos.bin'),
            os.path.join(current_dir, 'cppos.bin'),
            # From executable directory (if bundled)
            os.path.join(os.path.dirname(sys.executable), 'cppos.bin'),
            os.path.join(os.path.dirname(sys.executable), 'releases', 'cppos.bin'),
            # From script directory
            os.path.join(launcher_dir, 'cppos.bin'),
            # Relative paths
            'releases/cppos.bin',
            'build/cppos.bin',
            '../releases/cppos.bin',
            '../build/cppos.bin',
            '../../releases/cppos.bin',
            '../../build/cppos.bin',
        ]
        
        for path in possible_paths:
            abs_path = os.path.abspath(path)
            self.log(f"  Checking: {abs_path}")
            if os.path.exists(abs_path):
                self.kernel_path = abs_path
                self.kernel_status.config(
                    text=f"✅ Kernel: {self.kernel_path}", 
                    foreground="green"
                )
                self.log(f"✓ Found kernel: {self.kernel_path}")
                self.update_run_button()
                return
        
        # If not found, check for embedded data
        if CPPOS_KERNEL_BASE64.strip() and not CPPOS_KERNEL_BASE64.strip().startswith('#'):
            # Extract embedded kernel to temp file
            import base64
            temp_dir = tempfile.gettempdir()
            kernel_path = os.path.join(temp_dir, 'cppos.bin')
            try:
                with open(kernel_path, 'wb') as f:
                    f.write(base64.b64decode(CPPOS_KERNEL_BASE64))
                self.kernel_path = kernel_path
                self.kernel_status.config(
                    text=f"✅ Kernel: Embedded (extracted to {kernel_path})",
                    foreground="green"
                )
                self.log("✓ Using embedded kernel")
                self.update_run_button()
                return
            except Exception as e:
                self.log(f"Error extracting kernel: {e}")
        
        self.kernel_status.config(text="❌ Kernel: Not found", foreground="red")
        self.log("✗ ERROR: Kernel binary not found!")
        self.log("")
        self.log("The kernel (cppos.bin) needs to be built first.")
        self.log("Searched locations:")
        for path in possible_paths[:6]:
            self.log(f"  - {os.path.abspath(path)}")
        
    def update_run_button(self):
        """Enable run button if both QEMU and kernel are found"""
        if self.qemu_path and self.kernel_path:
            self.run_button.config(state=tk.NORMAL)
            self.log("Ready to run! Click 'Run CppOS' button")
        
    def run_os(self):
        """Run CppOS with QEMU"""
        if not self.qemu_path or not self.kernel_path:
            messagebox.showerror("Error", "QEMU or kernel not found!")
            return
        
        self.run_button.config(state=tk.DISABLED)
        self.progress.start()
        self.log("Starting CppOS...")
        
        # Run QEMU in a separate thread
        thread = threading.Thread(target=self._run_qemu)
        thread.daemon = True
        thread.start()
        
    def _run_qemu(self):
        """Run QEMU process"""
        try:
            cmd = [
                self.qemu_path,
                '-kernel', self.kernel_path,
                '-serial', 'stdio',
                '-display', 'gtk' if self.platform != 'Windows' else 'sdl'
            ]
            
            self.log(f"Command: {' '.join(cmd)}")
            
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Read output
            for line in iter(self.process.stdout.readline, ''):
                if line:
                    self.root.after(0, lambda l=line: self.log(l.strip()))
            
            self.process.wait()
            
            if self.process.returncode == 0:
                self.root.after(0, lambda: self.log("CppOS exited normally"))
            else:
                self.root.after(0, lambda: self.log(f"CppOS exited with code {self.process.returncode}"))
                
        except Exception as e:
            self.root.after(0, lambda: self.log(f"Error: {str(e)}"))
        finally:
            self.root.after(0, self._run_finished)
            
    def _run_finished(self):
        """Called when QEMU process finishes"""
        self.progress.stop()
        self.run_button.config(state=tk.NORMAL)
        self.process = None
        
    def stop_os(self):
        """Stop QEMU process"""
        if self.process:
            self.log("Stopping CppOS...")
            try:
                self.process.terminate()
                self.process.wait(timeout=2)
            except:
                self.process.kill()
            self.process = None
            self._run_finished()
        else:
            self.log("No process running")
            
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About CppOS Launcher",
            "CppOS Launcher v1.0\n\n"
            "A simple GUI launcher for CppOS - C++ Operating System\n\n"
            "Requirements:\n"
            "- QEMU (qemu-system-i386)\n"
            "- CppOS kernel binary (cppos.bin)\n\n"
            "The launcher will automatically find QEMU in PATH\n"
            "or common installation directories."
        )

def main():
    root = tk.Tk()
    app = CppOSLauncher(root)
    root.mainloop()

if __name__ == '__main__':
    main()
