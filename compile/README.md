# Compiler
The structure of the compiler largely builds forth on that of the interpreter; that's also to be seen in the used folder and code structure and the compiled assembly code. Just as with the compiler, we have a context that holds all symbols. Except it now also contains registers and segments that can be taken and restored. The function remains practically the same since it's just a container of code. 

Then, the compiler. The funny thing is that the code is still kind of interpreted; calculations are still being made, variables are still being assigned and function calls still occur. The only difference is that functions, while-loops and if-statements aren't executed; instead, they're compiled into assembly code and written into a file.

## Assembly
This structure seeps through in the compiled assembly code. The piece of SRPL code underneath translates to the assembly code underneath the code snippet.
```
variable n is n min 1 end 
```
Hence, one can conlude that the generated assembly code is a 1 to 1 copy of the SRPL source code. Register 5 is equal to the literal value 1 and n is decremented.
``` asm
movs	r5, #1
sub 	r0, r5
```

Another 'smart resemblance' is the way if-statements are taken care of. Instead of using all 'branch if...' instructions such as bgt, ble, beq, SRPL only uses bne after a compare statement between the condition and the literal value 1.
``` SRPL
n is_greater_than_or_equal_to 1
```
Hence, the codesnippet above literally translates to the assembly underneath. This has the advantage of not having to differentiate between conditions and variables representing a boolean.
``` asm
movs	r2, #1
asr 	r3, r0, #31
lsr 	r4, r2, #31
cmp 	r0, r2
adc 	r3, r3, r4
cmp 	r3, #1
bne 	end
```