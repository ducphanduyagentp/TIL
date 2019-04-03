# Browser Exploitation

## v8

### Leaking addresses

- There are at least 2 ways to leak address to glibc (and eventually stack after leaking `environ`)
    - Through native functions
        - Leaking address to native functions like `Array`
        - Getting the pointer to its code
        - There will be a built-in pointer in the first few instructions. This address points to a function in libv8.so
        - From this address, we can find the GOT entry of `__cxa_finalize` in libv8.so. This will point to glibc
        - From there we can get the `environ` address in glibc and leak stack addresses
    - Through a variable address (haven't checked universally)
        - After getting an address of a variable, there is a pointer in the first few values of the page that eventually dereferences to an address in libv8.so. This is some C++ function
        - After getting this address, do the same as the method above to get `__cxa_finalize`
    - When searching for GOT offset in libv8.so, need to grep for `GLIBC_2.2.5 + 0` or something similar, using the `-a` flag.