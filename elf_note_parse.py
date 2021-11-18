#!/usr/bin/env python3

"""
Parse a specified SH_NOTE section from an ELF and print it.

See also `llvm-readelf -n`.
"""

import struct
import sys

# get data from the elf. hold on tight.
from elftools.elf.elffile import ELFFile


def parse_notes_section(binary):
    """Parse binary data for a notes section"""
    # unpack header
    namesz, descsz, type_id = struct.unpack("<III", binary[:12])

    binary = binary[12:]

    print(f"---\n{'type'}: {type_id}")

    for field, value in {"namesz": namesz, "descsz": descsz}.items():
        print(f"---\n{field}: {value}")
        if value > 0:
            data = binary[:value]
            print(repr(data))
            print(data.hex())

            # 4-byte align each section
            # see https://docs.oracle.com/cd/E23824_01/html/819-0690/chapter6-18048.html
            rem = value % 4
            value = value + (4 - rem) if rem else value
            binary = binary[value:]


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <elf> <section name>")
        sys.exit(1)

    with open(sys.argv[1], "rb") as elffile:
        elf = ELFFile(elffile)
        for section in elf.iter_sections():
            if section.name == sys.argv[2]:
                print(section.name)
                parse_notes_section(section.data())
