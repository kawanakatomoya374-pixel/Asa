#!/bin/bash
# build.sh - Cross-platform build script for CppOS
# Works on Linux, macOS, and MSYS2/MinGW on Windows

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  CppOS Build Script${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
else
    OS="unknown"
fi

echo "Detected OS: $OS"
echo ""

# Check required tools
check_tool() {
    if ! command -v $1 &> /dev/null; then
        echo -e "${RED}[ERROR] $1 is not installed${NC}"
        return 1
    else
        echo -e "${GREEN}[OK] $1 found${NC}"
        return 0
    fi
}

echo "Checking build tools..."
MISSING=0

check_tool nasm || MISSING=1
check_tool g++ || MISSING=1
check_tool ld || MISSING=1

if [ $MISSING -ne 0 ]; then
    echo ""
    echo -e "${RED}Please install missing tools:${NC}"
    if [ "$OS" == "linux" ]; then
        echo "  Ubuntu/Debian: sudo apt-get install gcc g++ nasm make qemu-system-x86"
        echo "  Fedora:        sudo dnf install gcc gcc-c++ nasm make qemu-system-x86"
    elif [ "$OS" == "macos" ]; then
        echo "  brew install nasm qemu"
    elif [ "$OS" == "windows" ]; then
        echo "  pacman -S gcc nasm make mingw-w64-x86_64-gcc"
    fi
    exit 1
fi

echo ""

# Create build directory
mkdir -p build/kernel build/boot

# Assemble bootloader
echo -e "${YELLOW}[BUILD] Assembling bootloader...${NC}"
nasm -f elf32 src/boot/boot.asm -o build/boot/boot.o

# Compile kernel C++ files
echo -e "${YELLOW}[BUILD] Compiling kernel...${NC}"
CXXFLAGS="-m32 -ffreestanding -O2 -Wall -Wextra -fno-exceptions -fno-rtti -nostdlib -nostartfiles -I./src/kernel"

for file in src/kernel/*.cpp; do
    obj="build/kernel/$(basename $file .cpp).o"
    echo "  CC $file -> $obj"
    g++ $CXXFLAGS -c "$file" -o "$obj"
done

# Link kernel
echo -e "${YELLOW}[BUILD] Linking kernel...${NC}"
ld -m elf_i386 -T src/kernel/linker.ld -nostdlib \
    -o build/cppos.bin \
    build/boot/boot.o \
    build/kernel/*.o

# Verify multiboot2
echo -e "${YELLOW}[CHECK] Verifying Multiboot2...${NC}"
if command -v grub-file &> /dev/null; then
    if grub-file --is-x86-multiboot2 build/cppos.bin; then
        echo -e "${GREEN}[OK] Valid Multiboot2 kernel${NC}"
    else
        echo -e "${RED}[WARN] Multiboot2 validation failed${NC}"
    fi
else
    echo -e "${YELLOW}[SKIP] grub-file not available${NC}"
fi

# Copy to releases
cp build/cppos.bin releases/cppos.bin 2>/dev/null || true

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Build successful!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Kernel binary: build/cppos.bin"
echo ""
echo "To run with QEMU:"
echo "  ./run.sh"
echo "  make run"
echo "  qemu-system-i386 -kernel build/cppos.bin"
