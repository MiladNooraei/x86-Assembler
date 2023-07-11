
# x86-Assembler

A simple x86 Assembler which converts x86 Assembly instructions to machine code
## Description
In this project we get an x86 Assembly instruction (ADD, SUB, AND, OR) as input and get machine code as output.
## Example

Here are some input and output examples :

```bash
Please enter your assembly code:
ADD eax, ecx
Your machine code:
\x01\xc8
```
```bash
Please enter your assembly code:
ADD eax, [ebx] 
Your machine code: 
\x03\x3
```
```bash
Please enter your assembly code:
SUB [ecx], edx
Your machine code:
\x29\x11
```
