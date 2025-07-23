cmake_minimum_required(VERSION 3.20)
project(PrimusBoot C CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Set output directory for .efi binary
# set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/esp/EFI/Boot)

# set(ESP_DIR "${CMAKE_SOURCE_DIR}/esp")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/esp/EFI/Boot)
add_executable(BOOTX64.efi
    src/main.cc
    /usr/lib/crt0-efi-x86_64.o
)

# Optional: reinforce output directory (but now placed after target exists)
set_target_properties(BOOTX64.efi PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/esp/EFI/Boot
)

target_compile_options(BOOTX64.efi PRIVATE
    -fno-stack-protector
    -fpic
    -fshort-wchar
    -mno-red-zone
    -Wall
)

target_include_directories(BOOTX64.efi PRIVATE
    /usr/include/efi
    /usr/include/efi/x86_64
)

target_link_options(BOOTX64.efi PRIVATE
    -nostdlib
    -Wl,-e,efi_main
    -Wl,-T,${CMAKE_SOURCE_DIR}/scripts/elf_x86_64_efi.lds
    -Wl,--gc-sections
    -Wl,-Bsymbolic
    -Wl,--no-check-sections
    -Wl,--no-relax
)



target_link_libraries(BOOTX64.efi
    PRIVATE
        /usr/lib/libefi.a
        /usr/lib/libgnuefi.a
)
