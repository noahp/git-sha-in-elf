#!/usr/bin/env python3

"""
Generate a section header + contents for a note section.

Specify `--header` third argument to print the header only.
"""

import struct
import sys


def generate_elf_note(name, section_data, header):
    """Generate an elf note section for the specified data + description. If
    header==True, don't include the description data in the output"""
    output = struct.pack(
        "<III",
        len(name) + 1,
        len(section_data),  # not null termed
        0x10,  # random type
    )

    # pad to 4-byte alignment
    rem = (len(name) + 1) % 4
    append = b"\0" * (4 - rem) if rem else b""
    output += bytes(name, encoding="ascii", errors="ignore") + b"\0" + append
    if not header:
        output += bytes(section_data, encoding="ascii", errors="ignore")

    return output


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <note name> <section data string> [--header]")
        sys.exit(1)

    header_ = len(sys.argv) == 4 and sys.argv[3] == "--header"

    name_, section_data_ = sys.argv[1], sys.argv[2]

    output_ = generate_elf_note(name_, section_data_, header_)

    sys.stdout.buffer.write(output_)
