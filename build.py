import os
import subprocess
import shutil
import sys

build_dir = "build"
esp_dir = os.path.join(build_dir, "esp", "EFI", "Boot")
output_img = os.path.join(build_dir, "boot.img")
boot_efi = os.path.join(esp_dir, "BOOTX64.efi")

os.makedirs(esp_dir, exist_ok=True)

subprocess.run([
    "cmake",
    "-B", build_dir,
    "-DCMAKE_TOOLCHAIN_FILE=cmake/Toolchain.cmake"
], check=True)

subprocess.run([
    "cmake", "--build", build_dir
], check=True)

if os.path.exists(output_img):
    os.remove(output_img)

subprocess.run([
    "mkfs.vfat", "-C", output_img, "65536"
], check=True)

subprocess.run([
    "mcopy", "-i", output_img, "-s",
    os.path.join(build_dir, "esp", "EFI"),
    "::/EFI"
], check=True)

ovmf_code = "/usr/share/edk2/x64/OVMF_CODE.4m.fd"
ovmf_vars = "OVMF_VARS.fd"  

if not os.path.exists(ovmf_vars):
    print(f"Missing {ovmf_vars}. Copy it from /usr/share/edk2/x64/OVMF_VARS.4m.fd")
    sys.exit(1)

subprocess.run([
    "qemu-system-x86_64",
    "-drive", f"if=pflash,format=raw,readonly=on,file={ovmf_code}",
    "-drive", f"if=pflash,format=raw,file={ovmf_vars}",
    "-drive", f"format=raw,file={output_img},if=virtio",
    "-serial", "mon:stdio"
])
