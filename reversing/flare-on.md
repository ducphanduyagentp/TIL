# Flare-on

## FLARE-ON 5 challenge #5 - 08312018

### What the wasm binary is trying to do

- Takes in 2 buffer and their length, the first one is hardcoded from the js code.
- Iterate through the characters in the hardcoded buffer. Each character will decide a function call on the remaining of the buffers.
- The length of the flag is not equal to the length of the hardcoded buffer. The matching algorithm uses a pointer and may consume several bytes from the pointer in 1 function call.
- The flag is 33-char long (!?) (based on the number of function call happened)
- Function call orders
        5
        1
        5
        7
        2
        5
        1
        3
        7
        2
        7
        4
        4
        2
        7
        6
        4
        2
        2
        1
        7
        7
        5
        1
        4
        3
        1
        4
        2
        6
        5
        4
        6
- Turns out each function just carries out some types of encoding and compare the input buffer with the return value from the function. We just need to set a breakpoint and grab all the characters from the flag.

```
Microsoft Windows [Version 10.0.17134.228]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Users\ptneg>python
Python 2.7.15 (v2.7.15:ca079a3ea3, Apr 30 2018, 16:30:26) [MSC v.1500 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> ord('A')
65
>>> chr(119)
'w'
>>> x=[119,97,115,109,95,114,117,108,101,122,95]
>>> [chr(z) for z in x]
['w', 'a', 's', 'm', '_', 'r', 'u', 'l', 'e', 'z', '_']
>>> x=[119,97,115,109,95,114,117,108,101,122,95,106,115,95,100,114,111,111,108,122,64,102,108,97,114,101,45,111,110,46,99,111,109]
>>> [chr(z) for z in x]
['w', 'a', 's', 'm', '_', 'r', 'u', 'l', 'e', 'z', '_', 'j', 's', '_', 'd', 'r', 'o', 'o', 'l', 'z', '@', 'f', 'l', 'a', 'r', 'e', '-', 'o', 'n', '.', 'c', 'o', 'm']
>>> ''.join([chr(z) for z in x])
'wasm_rulez_js_droolz@flare-on.com'
>>>
^C
C:\Users\ptneg>
```

## Magic - FlareOn5 - 09062918

- The program does dynamic code execution. There is a RWX data segment that will be decrypted to code to be called later in the program.
- In the unpack function, there is a check of the input length against a series of value.
- If the above check is passed, XOR decryption happens.
- The dynamic function call then happens. If the returned value doesn't pass the check, it encrypts the code again and return false.
- Exfiltrate function data:
    - Use manticore to extract addresses and other params to function calls.
    - Didn't work because I probably don't know how to use these symbollic execution engines
    - Manually parsed the data, because IDA decomplication got something wrong
- There are several types of check functions:
    - Calculate the n_th fibonacci number with n = ord(c)
    - Do simple arithmetic checking (equals, +13, ^0x2a)
    - AND operation
    - Short constants
    - Long constants
- Each password has 69 characters and they are checked by parts.
- And here comes r2pipe for dynamic analysis.
    - set breakpoints when the comparisons happen and get the correct value of the character, then work out the input string
    - also dumping the decrypted code can be done easily :)
- There are only 6 function calls to complicated maths. Others are trivial.