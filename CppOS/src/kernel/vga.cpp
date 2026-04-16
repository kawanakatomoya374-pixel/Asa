// vga.cpp - VGA text mode driver implementation
#include "vga.hpp"

namespace cppos {

void VGADriver::clear() {
    for (int y = 0; y < HEIGHT; y++) {
        for (int x = 0; x < WIDTH; x++) {
            buffer_[y * WIDTH + x] = (color_ << 8) | ' ';
        }
    }
    row_ = 0;
    col_ = 0;
    updateCursor();
}

void VGADriver::putc(char c) {
    if (c == '\n') {
        col_ = 0;
        row_++;
        if (row_ >= HEIGHT) {
            scroll();
        }
        updateCursor();
        return;
    }

    if (c == '\r') {
        col_ = 0;
        updateCursor();
        return;
    }

    if (c == '\t') {
        int spaces = 4 - (col_ % 4);
        for (int i = 0; i < spaces; i++) {
            putc(' ');
        }
        return;
    }

    buffer_[row_ * WIDTH + col_] = (color_ << 8) | (uint8_t)c;
    col_++;

    if (col_ >= WIDTH) {
        col_ = 0;
        row_++;
        if (row_ >= HEIGHT) {
            scroll();
        }
    }
    updateCursor();
}

void VGADriver::puts(const char* str) {
    for (size_t i = 0; str[i] != '\0'; i++) {
        putc(str[i]);
    }
}

void VGADriver::moveCursor(int x, int y) {
    if (x >= 0 && x < WIDTH && y >= 0 && y < HEIGHT) {
        col_ = x;
        row_ = y;
        updateCursor();
    }
}

void VGADriver::scroll() {
    // Move all lines up
    for (int y = 0; y < HEIGHT - 1; y++) {
        for (int x = 0; x < WIDTH; x++) {
            buffer_[y * WIDTH + x] = buffer_[(y + 1) * WIDTH + x];
        }
    }

    // Clear last line
    for (int x = 0; x < WIDTH; x++) {
        buffer_[(HEIGHT - 1) * WIDTH + x] = (color_ << 8) | ' ';
    }

    row_ = HEIGHT - 1;
    col_ = 0;
}

void VGADriver::updateCursor() {
    // Cursor position is linear: row * WIDTH + col
    uint16_t pos = row_ * WIDTH + col_;

    // VGA cursor index registers
    const uint16_t VGA_CTRL = 0x3D4;
    const uint16_t VGA_DATA = 0x3D5;

    // High byte
    __asm__ volatile ("outb %0, %1" : : "a"((uint8_t)0x0E), "Nd"(VGA_CTRL));
    __asm__ volatile ("outb %0, %1" : : "a"((uint8_t)((pos >> 8) & 0xFF)), "Nd"(VGA_DATA));

    // Low byte
    __asm__ volatile ("outb %0, %1" : : "a"((uint8_t)0x0F), "Nd"(VGA_CTRL));
    __asm__ volatile ("outb %0, %1" : : "a"((uint8_t)(pos & 0xFF)), "Nd"(VGA_DATA));
}

} // namespace cppos
