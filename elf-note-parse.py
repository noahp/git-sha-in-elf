import sys
import struct

# get data from the elf. hold on tight.
from elftools.elf.elffile import ELFFile


def parse_notes_section(binary):
    # unpack header
    namesz, descsz, type = struct.unpack("<III", binary[:12])

    binary = binary[12:]

    for field, value in {"namesz": namesz, "descsz": descsz}.items():
        print("---\n{}: {}".format(field, value))
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
        print("Usage: %s <elf> <section name>" % sys.argv[0])
        sys.exit(1)

    with open(sys.argv[1], 'rb') as elffile:
        elf = ELFFile(elffile)
        for section in elf.iter_sections():
            if section.name == sys.argv[2]:
                print(section.name)
                parse_notes_section(section.data())
    # output = struct.pack(
    #     "<III",
    #     len("GIT_SHA") + 1,
    #     len("97a30d5e086697cd335e22af6703fabbd3020ae7") + 1,
    #     0x10,  # random type
    # )

    # rem = (len("GIT_SHA") + 1) % 4
    # append = b"\0" * (4 - rem) if rem else b""
    # output += b"GIT_SHA\0" + append

    # sys.stdout.buffer.write(output)
