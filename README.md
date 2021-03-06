# SRPL
## Non code like language
Litteraly everybody working in IT has *at least touched* code once and is able to write a simple Hello World program. It is however, a common occurance that it's hard for people to explain to interested non-IT people (for example family members) what they're doing on a daily basis. Most languages feature all kinds of fancy operators and syntax requirements that're very powerful, but prevent non-IT people from trying a little something out themselves. In these kind of situations, SRPL comes into play; the SupeR simPle Language!

> **Course requirements**: Check the [course](COURSE.md) markdown file for description of meeting course requirements.

## Features
### Shell, Interpreter and Compiler
SRPL can interpret a file, can be used as a shell and is able to compile files to assembly.
To start the shell, execute ```python srpl.py``` in the commandline.
To run 'main.srpl' execute ```python srpl.py main.srpl``` in the commandline. Please note that the newlines can be replaced by semicolons and that every line in the file needs to end with a space.
To compile an SRPL sourcefile, execute ```python srpl.py example/source/even.srpl example/source/even.asm```. The SRPL sourcecode in even.srpl will then be compiled to assembly in even.asm. For large code-bases one can (luckily) compile all SRPL source files in any parent-directory by executing ```compile``` in the SRPL shell.

### Compiler
The compiler has been written with compatibility and simplicity in mind; it's very efficient most of the times, but for example the checking of conditions is done in such a way that it's easier to read than it is fast. This checking of conditions is done by first storing the boolean representation in a register and then checking for it being larger than 0. This could also have been done with a more complex branch statement, but hey; the method described above is very suited to the ideology behind SRPL.

Furthermore, only the really used registers are pushed to the stack and there's a neat optimization that recognizes registers being used in either case of an if-statement. This results in registers being allowed to be used in both the if- and else-statement. Other than that, there's one more feature that's very suited to SRPL; informative comment generation. This allows for easy checks of the compiled assembly files.

Last but not least, the compiler has been tested extensively with the help of unit-tests. These can be found in the [example directory](example) and can be compiled with the ```compile``` command in the SRPL shell.

### Documentation
Everything has been documented with usability and neccesity in mind. This boils down to not documenting every method or function, but just making sure every 'type' of function has at least been documented once. Documenting every operator of a number for example, would be useless and even distracting.

### Float and Int
The heart of this language is the number. Numbers can be an integer or a float. Furthermore, a ```true``` is seen as a Number larger than 0.
``` SRPL
flush 5.3 plus 4 
variable day is 6 
flush day is_larger_than_or_equal_to 5 
```
### Math
Of course a language should support simple math with taking the order of operations into account.
``` SRPL
variable sum is 5 plus 3 
variable product is sum multiplied_by 3
variable part is product divided_by 2.1 
variable freezing is part min 90 
```
### Functions
Functions (when interpreted) can have zero or more parameters and can return zero or more values. Furthermore, a file can contain multiple functions.
``` SRPL
task add with a and b contains 
	flush a plus b end 

variable sum is execute add with 3 and 5 now
flush sum
```
### While-loops
While-loops are fully supported. An error is printed when loop is infinite.
``` SRPL
variable i is 1 
while i is_less_than 5 then 
	variable i is i plus 1 end 

flush i 
```
### For-loops
For-loops are fully supported as of version 2.1. Not just a simple version though; with custom stepsize that can be both positive or negative.
``` SRPL
task fact with n contains 
	variable result is 1 
	for variable i is 2 to n then 
		variable result is result multiplied_by i end 
	flush result end 
```
### If-statements
If statements can have an optional else statement. Furthermore, all conventional conditions are supported.
For a complete list; check out [tokens.py](lex/token.py).
``` SRPL
variable fun is 5 
flush if fun is_greater_than 8 then ; 22 else 10 end
```
### Lambdas
Functions are first-class citizens; they can be stored in variables and passed to functions.
``` SRPL
task apply with number and lambda contains 
	execute lambda with number now end 

task makeTwenty with n contains 
	variable n is 20 
	flush n end 

variable applyCopy is apply 
variable wasntTwenty is 18 
variable wasntTwenty is execute applyCopy with wastnZero & makeTwenty now 
flush wasntTwenty 
```
### Multi-return
Unlike most other languages, functions and the file can return multiple values. This has been done since it's more natural to non-it people. Executing multiple tasks yields multiple results; not one single. As one can imagine, this doesn't work when it's compiled to assembly. Then only the last return statement is effective.
``` SRPL
task multi contains 
    flush 3 
    flush 5

execute multi now 
```
### Error handling
Error handling is also a little less conventional. It is able to determine when things are missing and it prints an error message in the terminal, but it still tries to continue. Very life-like again; when you fall with the bike on your way to the train-station, you (hopefully) stand up and continue your commute. You don't end your day there... If you're curious as to how this functions; try it out yourself.

## Example
``` SRPL

task add with a and b contains 
	flush a plus b end 

variable result is execute add with 3 & 5 now 
variable sum is add 
variable otherResult is execute sum with 4 & 5 now 
flush result 
flush otherResult 

variable i is 1 
while i is_less_than 5 then 
	variable i is i plus 1 end 
flush i 

task odd with n contains 
	flush if n is_equal_to 0 then 
	0 else execute even with n min 1 now end end 

task even with n contains 
	flush if n is_equal_to 0 then 
	1 else execute odd with n min 1 now end end 

variable evenCopy is even 

flush execute even with 4 now 
flush execute odd with 4 now 
flush execute evenCopy with 3 now 
flush execute odd with 3 now 

task apply with number and lambda contains 
	execute lambda with number now end 

task makeTwenty with n contains 
	variable n is 20 
	flush n end 

variable wasntTwenty is 18 
variable wasntTwenty is execute apply with wastnZero & makeTwenty now 
flush wasntTwenty 

task sommig with n contains 
	variable result is 0 
	while n is_greater_than_or_equal_to 1 then 
		variable result is result plus n 
		variable n is n min 1 end 
	flush result end 
 
flush execute sommig with 5 now 
flush execute sommig with 34 now 
 
task fact with n contains 
	variable result is 1 
	for variable i is 2 to n plus 1 then 
		variable result is result multiplied_by i end 
	flush result end 

flush execute fact with 5 now 
flush i 

task neg_for with n contains 
	variable result is 1 
	for variable i is 10 to 0 step 0 min 2 then 
		variable result is result plus i end 
	flush result end 

flush execute neg_for with 5 now 
```

> **Output**: ```[8, 9, 5, 1, 0, 0, 1, 20, 15, 595, 120, 5, 31]```