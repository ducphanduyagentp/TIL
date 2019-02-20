# pwnable.tw

## pwnable.tw applestore - 07312018

- Cart is stored as a doubly-linked list, starting from the `myCart` address
- If the value of the cart equals to 7174, add an iPhone 8 to the cart, making it 7175. However, the address of the iPhone 8 is on the stack
    - ==> It's trying to persist a stack address outside the scope of a function
    - There's malloc but no free
    - It's using asprintf to write to strings.
- Item struct
    ```C
    struct cartItem {
        char *itemName;
        int itemValue;
        struct cartItem *nextPtr;
        struct cartItem *prevPtr;
    }
    ```
- Functions
    - add: Call to create and insert to add a new item to cart.
    - create: alloc 0x10 bytes for a cartItem struct, then write the item's name and value to the first 2 fields of the instance.
    - insert: link the new Item to the doubly-linked list by placing pointers to the last 2 fields of the instance.
    - delete: iterate the linked list using the index. When the correct index is reached, carry out the unlink on the doubly-linked list:
        - If P->prev != 0: P->prev->next = P->next
        - If P->next !- 0: P->next->prev = P->prev
    - cart: 
    - checkout
- The `my_read` function leaves extra data on the stack, will can be used in conjunction with the stack address stored in the linked list to leak libc address
    - Add 6 items 1 to cart
    - Add 20 items 2 to cart
    - Checkout so it adds the iPhone 8 (stack address) to the linked list
    - now we can fake an item by inserting extra data when being asked for choices or indices
- Where can I write to: arbitrary address in writable segments.
- What can I write: addresses of writable segments. So not code, because of the unlink feature acting on a doubly linked list.
- What and where do I need to write:
    - Arbitrary data to a GOT entry, ideally atoi.
- What I did not notice
    - How to leak data at an arbitrary address using the extra data in the **index** of a device. This is because I didn't notice the relation between the stack address of the command portion and the index portion
    - Code reuse in the _handler_ function. Since the unlink feature only allow writing to writeable segments, it is not possible (afaik) to directly overwrite the GOT entry with the address of system (a code segment address, not writable in NX is enabled). The unlink feature cannot be used to directly overwrite the GOT entry, but to overwrite an address of a buffer that data will be read in, with the address of a GOT entry.
    - To be able to leak a stack address, I used the firstItem pointer following the myCart symbol. In one of the writeup, the author mention the usage of the `environ` symbol in libc, which can be used (universally?) to leak stack address. It is detailed in the CTF-pwn-tips repo.


## pwnable.tw hacknote - 07122018

- There is a global array with 5 elements. Each contains a pointer to a struct Note
- Struct Note
    ```
    typedef struct Note {
        void (*func)(char *str);
        char *content;
    } Note;
    ```
- Exploitation plan
    - Since the addNote function is buggy, even if the note is deleted, you can only alloc 5 times in total
    - Alloc 2 note, then trigger double free to prepare the fastbin attack
    - Alloc 1 note. This will be the chunk that we're creating fake chunk
    - Create a fake chunk with the first pointer point to system, the second one point to "/bin/sh"
- That exploitation plan will not work because it takes at least 6 mallocs to take control of the desired pointer. I've come up with a different one.
    - Alloc chunk A: 1024
    - Alloc chunk B: 100
    - Free chunk B
    - Free chunk A
    - Now we are able to leak main_arena in chunk A's data
    - Alloc chunk C, same size as chunk A / 1024. Write 4 bytes
    - Print chunk C => main_arena get printed.
    - Free chunk C
    - Alloc chunk D / 1080, but with larger size so that it stays in the same bin as chunk B. Overflow to the data into chunk B's data to overwrite the address of the putsWrapper function to system and the pointer of the string to "/bin/sh". Or we can keep /bin/sh. But this requires leaking heap address.
    - Print chunk B (Use-After-Free) => system("/bin/sh") is called. pwned.

## pwnable.tw silver_bullet - 07292018

- This is an off-by-one overflow on the stack
- The createBullet function read in a buffer of 48 char maximum.
    - The string is saved on the stack (local var in main)
    - The length of the string is stored right after the string on the stack. The power of the bullet is the dword (4byte) that is right after the string.
- The powerUp function read in a string of length based on the current length stored on the stack, and then concat the input with the string on the stack
    - strncat append the src string to the dest string **THEN** place a null byte after the new string
        - len(dest) = x
        - len(src) = 48 - x
        - ==> dest[48] == bullet's strength == NULL after concat
    - Then it take dword(dest[48]) and add the length of the src string, store it at dest[48] again
        - dword(dest[48]) = dword(dest[48]) + strlen(src)