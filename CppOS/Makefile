# CppOS Makefile
# C++ Operating System Build System

# Compiler and tools
CXX = g++
AS = nasm
LD = ld
QEMU = qemu-system-i386

# Flags
CXXFLAGS = -m32 -ffreestanding -O2 -Wall -Wextra -fno-exceptions -fno-rtti -nostdlib -nostartfiles
ASFLAGS = -f elf32
LDFLAGS = -m elf_i386 -T src/kernel/linker.ld -nostdlib

# Directories
SRC_DIR = src
BUILD_DIR = build
ISO_DIR = isodir

# Source files
CPP_SOURCES = $(wildcard $(SRC_DIR)/kernel/*.cpp)
ASM_SOURCES = $(wildcard $(SRC_DIR)/boot/*.asm)

# Object files
CPP_OBJECTS = $(patsubst $(SRC_DIR)/%.cpp,$(BUILD_DIR)/%.o,$(CPP_SOURCES))
ASM_OBJECTS = $(patsubst $(SRC_DIR)/%.asm,$(BUILD_DIR)/%.o,$(ASM_SOURCES))
OBJECTS = $(CPP_OBJECTS) $(ASM_OBJECTS)

# Target
KERNEL = $(BUILD_DIR)/cppos.bin
ISO = $(BUILD_DIR)/cppos.iso

# Default target
.PHONY: all clean run iso

all: $(KERNEL)

# Create build directories
$(BUILD_DIR)/kernel $(BUILD_DIR)/boot:
	mkdir -p $@

# Compile C++ sources
$(BUILD_DIR)/kernel/%.o: $(SRC_DIR)/kernel/%.cpp | $(BUILD_DIR)/kernel
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Assemble ASM sources
$(BUILD_DIR)/boot/%.o: $(SRC_DIR)/boot/%.asm | $(BUILD_DIR)/boot
	$(AS) $(ASFLAGS) $< -o $@

# Link kernel
$(KERNEL): $(OBJECTS) $(SRC_DIR)/kernel/linker.ld
	$(LD) $(LDFLAGS) -o $@ $(OBJECTS)
	# Verify multiboot
	grub-file --is-x86-multiboot2 $@ || (echo "Error: Not a valid multiboot2 kernel" && exit 1)
	@echo "Kernel built successfully: $@"

# Create ISO image
iso: $(ISO)

$(ISO): $(KERNEL)
	mkdir -p $(ISO_DIR)/boot/grub
	cp $(KERNEL) $(ISO_DIR)/boot/cppos.bin
	echo 'menuentry "CppOS" {' > $(ISO_DIR)/boot/grub/grub.cfg
	echo '    multiboot2 /boot/cppos.bin' >> $(ISO_DIR)/boot/grub/grub.cfg
	echo '}' >> $(ISO_DIR)/boot/grub/grub.cfg
	grub-mkrescue -o $(ISO) $(ISO_DIR)
	@echo "ISO created: $@"

# Run with QEMU
run: $(KERNEL)
	$(QEMU) -kernel $(KERNEL) -serial stdio

# Run ISO with QEMU
run-iso: $(ISO)
	$(QEMU) -cdrom $(ISO) -serial stdio

# Debug with QEMU
debug: $(KERNEL)
	$(QEMU) -kernel $(KERNEL) -serial stdio -s -S

# Clean build files
clean:
	rm -rf $(BUILD_DIR) $(ISO_DIR)
	@echo "Build files cleaned"

# Info
info:
	@echo "CppOS Build System"
	@echo "=================="
	@echo "Targets:"
	@echo "  all      - Build the kernel binary"
	@echo "  iso      - Create bootable ISO image"
	@echo "  run      - Run kernel with QEMU"
	@echo "  run-iso  - Run ISO with QEMU"
	@echo "  debug    - Run with GDB debugging support"
	@echo "  clean    - Clean all build files"
	@echo "  info     - Show this help"
