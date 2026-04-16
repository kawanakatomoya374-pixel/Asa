; boot.asm - Multiboot2 compliant bootloader
; This file sets up the basic environment and calls the kernel

section .multiboot_header
align 8
header_start:
    dd 0xe85250d6                ; Multiboot2 magic number
    dd 0                         ; Architecture (i386)
    dd header_end - header_start ; Header length
    dd 0x100000000 - (0xe85250d6 + 0 + (header_end - header_start)) ; Checksum

    ; End tag
    dw 0    ; type
    dw 0    ; flags
    dd 8    ; size
header_end:

section .bss
align 16
stack_bottom:
    resb 16384 ; 16 KiB stack
stack_top:

section .text
global start
extern kernel_main

start:
    ; Set up the stack
    mov esp, stack_top

    ; Save multiboot info
    push ebx    ; Multiboot info structure pointer
    push eax    ; Multiboot magic number

    ; Call the kernel main function
    call kernel_main

    ; If kernel_main returns, hang
    cli
.hang:
    hlt
    jmp .hang
