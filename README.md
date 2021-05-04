# SRPL
## Non code like language
Litteraly everybody working in IT has at least touched code once and is *at least* able to write a simple Hello World program. It is however, a common occurance that it's hard for people to explain to interested non-IT people (for example family members) what they're doing on a daily basis. Most languages feature all kinds of fancy operators and syntax requirements that prevent non-IT people from trying a little something out themselves. In these kind of situations, SRPL comes into play; the SupeR simPle Language!

## Language
| Type                  | Token                     |
| --------------------- |-------------------------- |
| Assignment            | is                        |
| Add operator          | plus                      |
| Substract operator    | min                       |
| Multiply operator     | multiplied_by             |
| Divide operator       | divided_by                |
| If                    | when                      |
| Else                  | else                      |
| Equalilty operator    | is_equal_to               |
| Non-Equality operator | is_not_equal_to           |
| Termination           | ]                         |
| Print                 | log                       |
| Greater than          | greater_than              |
| Greater than or equal | greater_than_or_equal_to  |
| Less than             | less_than                 |
| Less than or equal    | less_than_or_equal_to     |

## Example
``` SRPL
task add with a and b contains ; flush a plus b end
execute add with 3 & 5 now

variable i is 1
while i is_less_than 5 then ; variable i is i plus 1 end ; flush i

variable result is if 5 is_equal_to 3 then ; 2 else 4 end

task equalThree with n contains ; if n is_equal_to 3 then ; flush 3 else 0 end end
execute equalThree with 3 now

task odd with n contains ; if n is_equal_to 0 then ; flush 0 else ; variable n is n min 1 end ; flush execute even with n now end ;

task odd with n contains ; flush if n is_equal_to 0 then ; 0 else execute even with n min 1 now end end 
task even with n contains ; flush if n is_equal_to 0 then ; 1 else execute odd with n min 1 now end end
execute even with 2 now

task sommig with n contains ; variable result is 0 ; while n is_greater_than_or_equal_to 1 then ; variable result is result plus n ; variable n is n min 1 end ; flush result end
execute sommig with 5 now
```