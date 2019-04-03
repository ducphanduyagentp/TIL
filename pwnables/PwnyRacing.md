# Pwny Racing

## Challenge 1

- Binary has multiple functions being dynamically called based on the CRC values of the input
- A function call happens every 16 bytes
- Leak binary:
    - Enter new line so the debug variable is increased incorrectly and debug mode is enabled.
    - Enter Maximum characters so no null byte between input and funcs and funcs got dumped out.
- This means we can execute 64 functions in one attempt.
    - 128 after leak
- Can't overwrite GOT because of full RELRO
- Rewrite function table to system