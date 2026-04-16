// serial.cpp - Serial port driver implementation
#include "serial.hpp"

namespace cppos {

bool SerialDriver::init() {
    // Disable interrupts
    outb(port_ + INT_REG, 0x00);

    // Enable DLAB (set baud rate divisor)
    outb(port_ + LINE_REG, 0x80);

    // Set divisor to 3 (38400 baud)
    outb(port_ + DATA_REG, 0x03);
    outb(port_ + DATA_REG + 1, 0x00);

    // 8 bits, no parity, one stop bit
    outb(port_ + LINE_REG, 0x03);

    // Enable FIFO, clear them, with 14-byte threshold
    outb(port_ + FIFO_REG, 0xC7);

    // IRQs enabled, RTS/DSR set
    outb(port_ + MODEM_REG, 0x0B);

    // Set in loopback mode to test the serial chip
    outb(port_ + MODEM_REG, 0x1E);

    // Test serial chip (send 0xAE and check if we get same result)
    outb(port_ + DATA_REG, 0xAE);

    // Check if serial is faulty
    if (inb(port_ + DATA_REG) != 0xAE) {
        return false;
    }

    // If serial is not faulty, set it in normal operation mode
    outb(port_ + MODEM_REG, 0x0F);

    initialized_ = true;
    return true;
}

bool SerialDriver::isTransmitEmpty() {
    return (inb(port_ + LINE_STATUS_REG) & 0x20) != 0;
}

bool SerialDriver::dataAvailable() {
    return (inb(port_ + LINE_STATUS_REG) & 0x01) != 0;
}

void SerialDriver::putc(char c) {
    if (!initialized_) return;

    while (!isTransmitEmpty()) {
        // Busy wait
    }

    outb(port_ + DATA_REG, static_cast<uint8_t>(c));
}

void SerialDriver::puts(const char* str) {
    for (size_t i = 0; str[i] != '\0'; i++) {
        putc(str[i]);
    }
}

char SerialDriver::getc() {
    if (!initialized_) return '\0';

    while (!dataAvailable()) {
        // Busy wait
    }

    return static_cast<char>(inb(port_ + DATA_REG));
}

char SerialDriver::tryGetc() {
    if (!initialized_) return '\0';

    if (dataAvailable()) {
        return static_cast<char>(inb(port_ + DATA_REG));
    }

    return '\0';
}

void SerialDriver::write(const uint8_t* data, size_t length) {
    for (size_t i = 0; i < length; i++) {
        putc(static_cast<char>(data[i]));
    }
}

} // namespace cppos
