#!/bin/bash
# run.sh - Quick launcher for CppOS

echo "========================================"
echo "  CppOS - Quick Launcher"
echo "========================================"
echo ""

# Find kernel binary
KERNEL=""
if [ -f "build/cppos.bin" ]; then
    KERNEL="build/cppos.bin"
    echo "[OK] Found: build/cppos.bin"
elif [ -f "releases/cppos.bin" ]; then
    KERNEL="releases/cppos.bin"
    echo "[OK] Found: releases/cppos.bin"
else
    echo "[ERROR] Kernel not found!"
    echo ""
    echo "Please build first:"
    echo "  make"
    echo "  ./build.sh"
    echo ""
    exit 1
fi

echo ""
echo "Starting CppOS with QEMU..."
echo "(Press Ctrl+A then X to exit QEMU)"
echo ""

qemu-system-i386 -kernel "$KERNEL" -serial stdio
