// io.hpp - I/O port operations for CppOS
#ifndef CPPOS_IO_HPP
#define CPPOS_IO_HPP

#include <stdint.h>

namespace cppos {

// Output a byte to an I/O port
static inline void outb(uint16_t port, uint8_t value) {
    __asm__ volatile ("outb %0, %1" : : "a"(value), "Nd"(port));
}

// Input a byte from an I/O port
static inline uint8_t inb(uint16_t port) {
    uint8_t result;
    __asm__ volatile ("inb %1, %0" : "=a"(result) : "Nd"(port));
    return result;
}

// Output a word to an I/O port
static inline void outw(uint16_t port, uint16_t value) {
    __asm__ volatile ("outw %0, %1" : : "a"(value), "Nd"(port));
}

// Input a word from an I/O port
static inline uint16_t inw(uint16_t port) {
    uint16_t result;
    __asm__ volatile ("inw %1, %0" : "=a"(result) : "Nd"(port));
    return result;
}

// Output a long to an I/O port
static inline void outl(uint16_t port, uint32_t value) {
    __asm__ volatile ("outl %0, %1" : : "a"(value), "Nd"(port));
}

// Input a long from an I/O port
static inline uint32_t inl(uint16_t port) {
    uint32_t result;
    __asm__ volatile ("inl %1, %0" : "=a"(result) : "Nd"(port));
    return result;
}

// I/O wait (write to unused port 0x80)
static inline void io_wait() {
    outb(0x80, 0);
}

} // namespace cppos

#endif // CPPOS_IO_HPP
