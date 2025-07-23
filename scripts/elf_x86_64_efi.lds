OUTPUT_FORMAT("elf64-x86-64")
OUTPUT_ARCH(i386:x86-64)
ENTRY(efi_main)

SECTIONS {
    . = 0;

    .text : {
        *(.text*)
    } :text

    .sdata : {
        *(.sdata*)
    } :data

    .data : {
        *(.data*)
    } :data

    .dynamic : {
        *(.dynamic*)
    } :data

    .rodata : {
        *(.rodata*)
    } :data

    .bss : {
        *(.bss*)
        *(COMMON)
    } :data

    /DISCARD/ : {
        *(.note*)
        *(.comment*)
    }
}

PHDRS {
    text PT_LOAD FLAGS(5); /* R + X */
    data PT_LOAD FLAGS(6); /* R + W */
}
