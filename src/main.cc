#include <efi/efi.h>
#include <efi/efilib.h>

extern "C"
EFI_STATUS
efi_main(EFI_HANDLE image, EFI_SYSTEM_TABLE* system_table) {
    InitializeLib(image, system_table);
    Print((CHAR16*)L"Oblivion -1.0v\n");

    EFI_INPUT_KEY key;
    system_table->ConIn->ReadKeyStroke(system_table->ConIn, &key);

    return EFI_SUCCESS;
}