# SRPL
## Non code like language
Litteraly everybody working in IT has *at least touched* code once and is able to write a simple Hello World program. It is however, a common occurance that it's hard for people to explain to interested non-IT people (for example family members) what they're doing on a daily basis. Most languages feature all kinds of fancy operators and syntax requirements that're very powerful, but prevent non-IT people from trying a little something out themselves. In these kind of situations, SRPL comes into play; the SupeR simPle Language!

> **Course requirements**: Check the [course](COURSE.md) markdown file for description of meeting course requirements.

## Features
### Shell and File
SRPL can interpret a file, but can also be used as a shell.
To start shell, execute ```python srpl.py``` in the commandline.
To run 'main.srpl' execute ```python srpl.py main.srpl``` in the commandline.
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
Functions can have zero or more parameters and can return zero or more values. Furthermore, a file can contain multiple functions.
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
Unlike most other languages, functions and the file can return multiple values. This has been done since it's more natural to non-it people. Executing multiple tasks yields multiple results; not one single.
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

flush execute add with 3 & 5 now 

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
flush execute evenCopy with 5 now 

task summy with n contains 
	variable result is 0 
	while n is_greater_than_or_equal_to 1 then 
		variable result is result plus n 
		variable n is n min 1 end 
	flush result end 

flush execute summy with 5 now 
```