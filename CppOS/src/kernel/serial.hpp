// serial.hpp - Serial port (COM) driver for CppOS
#ifndef CPPOS_SERIAL_HPP
#define CPPOS_SERIAL_HPP

#include <stdint.h>
#include <stddef.h>
#include "io.hpp"

namespace cppos {

// COM port addresses
enum class COMPort : uint16_t {
    COM1 = 0x3F8,
    COM2 = 0x2F8,
    COM3 = 0x3E8,
    COM4 = 0x2E8
};

class SerialDriver {
public:
    explicit SerialDriver(COMPort port);

    // Initialize the serial port
    bool init();

    // Check if transmit buffer is empty
    bool isTransmitEmpty();

    // Check if data is available to read
    bool dataAvailable();

    // Write a single character
    void putc(char c);

    // Write a string
    void puts(const char* str);

    // Read a single character (blocking)
    char getc();

    // Read a character if available (non-blocking)
    char tryGetc();

    // Write raw bytes
    void write(const uint8_t* data, size_t length);

private:
    uint16_t port_;
    bool initialized_;

    static constexpr uint8_t DATA_REG = 0;
    static constexpr uint8_t INT_REG = 1;
    static constexpr uint8_t FIFO_REG = 2;
    static constexpr uint8_t LINE_REG = 3;
    static constexpr uint8_t MODEM_REG = 4;
    static constexpr uint8_t LINE_STATUS_REG = 5;
};

inline SerialDriver::SerialDriver(COMPort port)
    : port_(static_cast<uint16_t>(port)), initialized_(false) {
}

} // namespace cppos

#endif // CPPOS_SERIAL_HPP
