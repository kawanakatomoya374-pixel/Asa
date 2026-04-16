// kernel.cpp - C++ Kernel Main
#include "vga.hpp"
#include "serial.hpp"

using namespace cppos;

// Kernel main - entry point from bootloader
extern "C" void kernel_main() {
    // Initialize serial port for debugging
    SerialDriver serial(COMPort::COM1);
    serial.init();
    serial.puts("CppOS: Kernel started\n");

    // Initialize VGA driver
    VGADriver vga;
    vga.setColor(VGAColor::LightGreen, VGAColor::Black);
    vga.puts("=== CppOS v0.1 ===\n");
    vga.puts("C++ Operating System\n\n");

    vga.setColor(VGAColor::White, VGAColor::Black);
    vga.puts("Hello from C++ kernel!\n");
    vga.puts("Serial port initialized for debugging.\n");

    serial.puts("CppOS: Kernel initialization complete\n");
    serial.puts("CppOS: Running in C++ mode!\n");

    // Hang forever
    while (1) {
        __asm__ volatile ("hlt");
    }
}
