import os
import subprocess


build_dir = "build"
esp_path = os.path.join(build_dir, "esp/EFI/Boot")
output_img = "boot.img"

os.makedirs(esp_path, exist_ok=True)

subprocess.run(["cmake", "-B", "build", "-DCMAKE_TOOLCHAIN_FILE=cmake/Toolchain.cmake"], check=True)
subprocess.run(["cmake", "--build", "build"], check=True)

if os.path.exists(output_img):
    os.remove(output_img)

subprocess.run(["mkfs.vfat", "-C", output_img, "65536"], check=True)
subprocess.run(["mcopy", "-i", output_img, "-s", "esp", "::/"], check=True)

# subprocess.run([
#     "qemu-system-x86_64",
#     "-bios", "/usr/share/ovmf/x64/OVMF.fd",
#     "-drive", f"format=raw,file={output_img},if=virtio",
#     "-serial", "mon:stdio"
# ])
subprocess.run([
    "qemu-system-x86_64",
    "-drive", "if=pflash,format=raw,readonly=on,file=/usr/share/edk2/x64/OVMF_CODE.4m.fd",
    "-drive", "if=pflash,format=raw,file=OVMF_VARS.fd",  # you can make a writable copy of OVMF_VARS.4m.fd
    "-drive", f"format=raw,file={output_img},if=virtio",
    "-serial", "mon:stdio"
])