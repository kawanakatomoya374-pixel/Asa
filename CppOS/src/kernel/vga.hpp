// vga.hpp - VGA text mode driver for CppOS
#ifndef CPPOS_VGA_HPP
#define CPPOS_VGA_HPP

#include <stdint.h>
#include <stddef.h>

namespace cppos {

// VGA color codes
enum class VGAColor : uint8_t {
    Black = 0,
    Blue = 1,
    Green = 2,
    Cyan = 3,
    Red = 4,
    Magenta = 5,
    Brown = 6,
    LightGrey = 7,
    DarkGrey = 8,
    LightBlue = 9,
    LightGreen = 10,
    LightCyan = 11,
    LightRed = 12,
    LightMagenta = 13,
    LightBrown = 14,
    White = 15
};

class VGADriver {
public:
    static const int WIDTH = 80;
    static const int HEIGHT = 25;

    VGADriver();

    // Clear the screen
    void clear();

    // Write a character
    void putc(char c);

    // Write a string
    void puts(const char* str);

    // Set text color
    void setColor(VGAColor fg, VGAColor bg);

    // Move cursor to position
    void moveCursor(int x, int y);

    // Get current position
    int getX() const { return col_; }
    int getY() const { return row_; }

private:
    uint16_t* buffer_;
    int row_;
    int col_;
    uint8_t color_;

    void scroll();
    void updateCursor();
};

inline VGADriver::VGADriver()
    : buffer_((uint16_t*)0xB8000), row_(0), col_(0), color_(0x0F) {
    clear();
}

inline void VGADriver::setColor(VGAColor fg, VGAColor bg) {
    color_ = (static_cast<uint8_t>(bg) << 4) | static_cast<uint8_t>(fg);
}

} // namespace cppos

#endif // CPPOS_VGA_HPP
