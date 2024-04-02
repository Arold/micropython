import esp

SECTOR_NUMBER = 122
SECTOR_SIZE = 4096
BOOT_CODE_BUFFER_SIZE = 512


def read_boot_code():
    data = esp.flash_read(SECTOR_NUMBER * SECTOR_SIZE, BOOT_CODE_BUFFER_SIZE)
    if b"\x00" not in data:
        return ""
    else:
        return data.split(b"\x00")[0].decode()


def write_boot_code(code):
    code_encoded = code.encode()
    if b"\x00" in code_encoded:
        raise "0x00 in provided code. This symbol is reserved to determine code ending."
    reminder = len(code_encoded) % 4
    if reminder == 0:
        code_encoded += b"\x00\xff\xff\xff"
    elif reminder == 1:
        code_encoded += b"\x00\xff\xff"
    elif reminder == 2:
        code_encoded += b"\x00\xff"
    elif reminder == 3:
        code_encoded += b"\x00"

    esp.flash_erase(SECTOR_NUMBER)
    esp.flash_write(SECTOR_NUMBER * SECTOR_SIZE, code_encoded)
