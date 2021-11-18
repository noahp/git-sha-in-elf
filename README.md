# GIT SHA added to ELF file .note section

Example of adding a GIT SHA to an ELF file when linking a program.

Couple of python scripts:

- [`elf_-_note_-_parse.py`](elf_-_note_-_parse.py) - parses any "note" field from an
  elf, eg:

  ```bash
  ❯ ./elf_-_note_-_parse.py build/main .note.gnu.build-id
  .note.gnu.build-id
  ---
  namesz: 4
  b'GNU\x00'
  474e5500
  ---
  descsz: 20
  b'\x8c\x04/\x8e\xaf\x98{\xa3\xce\xab\xef\xfd\xce\\\xbb\x90G\xc20 '
  8c042f8eaf987ba3ceabeffdce5cbb9047c23020
  ```

- [`generate_-_elf_-_note.py`](generate_-_elf_-_note.py) - generates data for populating
  a `SH_NOTE` ELF section:

  ```bash
  ❯ ./generate-elf-note.py GIT_SHA $(git rev-parse HEAD) | xxd
  00000000: 0800 0000 2800 0000 1000 0000 4749 545f  ....(.......GIT_
  00000010: 5348 4100 6136 3339 3661 3835 6561 3735  SHA.a6396a85ea75
  00000020: 3462 3937 6237 3534 6330 3138 6630 3032  4b97b754c018f002
  00000030: 3664 6636 6330 3733 3866 6363            6df6c0738fcc
  ```

LLVM's readelf binutil does a good job of printing notes sections:

```bash
❯ llvm-readelf-12 --notes build/main
Displaying notes found in: .note.gnu.property
  Owner                Data size        Description
  GNU                  0x00000010       NT_GNU_PROPERTY_TYPE_0 (property note)
    Properties:    <application-specific type 0xc0008002>

Displaying notes found in: .note.gnu.build-id
  Owner                Data size        Description
  GNU                  0x00000014       NT_GNU_BUILD_ID (unique build ID bitstring)
    Build ID: df2e68644889e6f5672243d0e977592a8f5357c2
Displaying notes found in: .note.ABI-tag
  Owner                Data size        Description
  GNU                  0x00000010       NT_GNU_ABI_TAG (ABI version tag)
    OS: Linux, ABI: 3.2.0
Displaying notes found in: .note.gitsha
  Owner                Data size        Description
  GIT_SHA              0x00000028       Unknown note type: (0x00000010)
   description data: 61 36 33 39 36 61 38 35 65 61 37 35 34 62 39 37 62 37 35 34 63 30 31 38 66 30 30 32 36 64 66 36 63 30 37 33 38 66 63 63
```
