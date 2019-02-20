# Heap exploitation

## Fastbin attack

- The point is to return a nearly-arbitrary pointer
- Fastbin is LIFO, singly-linked list using the FD pointer
- When a malloc is requested and the size matches a fastbin size, it checks the chunk at the top of the bin.
    - The size of the chunk to be deleted from the bin must belong to that bin
- When a free is requested and the size matches a fastbin size, it checks the following.
    - The chunk at the top must not be the same as the chunk being freed to avoid double-free. But that's it. To bypass this, we only need to free some other chunk in between to not trigger this error. For example, free(a), free(b) and then we are able to free(a) again.
- After we triggered the double-free attack, we issue 2 malloc requests.
    - a and b will be allocated again. However, a is still on the free list at the same time.
    - With that in mind, we are able to modify the metadata, change the structure of the bin
    - We will take advantage of that to create a fake fast chunk. That fake chunk will point to the nearly-arbitrary address that we want to control.
    - The fake chunk can be created as following:
        - Overwrite the FD pointer of chunk a
        - Write a fake fast_size to the fake chunk so that it doesn't trigger the check "memory corruption (fast)" in malloc.

## Unlink attack

```C
#define unlink(AV, P, BK, FD) {                                            \
    FD = P->fd;								      \
    BK = P->bk;								      \
    if (__builtin_expect (FD->bk != P || BK->fd != P, 0))		      \
      malloc_printerr (check_action, "corrupted double-linked list", P, AV);  \
    else {								      \
        FD->bk = BK;							      \
        BK->fd = FD;
    ...	
```

- Typical scenario: There's a global pointer or some pointer that we've known it's address

## House of Force

- Prerequisite: 3 mallocs
    - 1st malloc: Know the address of the top chunk
    - 2nd malloc: arbitrary size
    - 3rd malloc: To overwrite data