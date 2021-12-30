#!/usr/bin/env python3

from subprocess import check_output, run
from os import path, remove
from re import findall


def get_shellcode(filename):
    file = filename.split(".")[0]

    if path.exists(filename):
        if run(["nasm", "-f elf", f"-o {file}.o", f"{filename}"]).returncode != 0\
        or run(["ld", "-m", "elf_i386", "-o", f"{file}", f"{file}.o"]).returncode !=0:
            raise RuntimeError
        data = check_output(["objdump", "-d", file]).decode()

    bytecode = findall(r"\b[0-9a-f]{2}\b", data)  # extract bytes
    remove(file)  # clean up
    remove(file + ".o")

    return bytearray([int(i, 16) for i in bytecode]),\
         f"Shellcode Length: {len(bytecode)}"

if __name__ == "__main__":
    
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("file", help="Path to .asm file")
    args = parser.parse_args()
    
    print((d := get_shellcode(args.file))[0])
    print("\n\n" + d[1])