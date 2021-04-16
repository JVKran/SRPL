# KRAN++
## Non code like language
Litteraly everybody working in IT has at least touched code once and is *at least* able to write a simple Hello World program. It is however, a common occurance that it's hard for people to explain to interested non-IT people (for example family members) what they're doing on a daily basis. Most languages feature all kinds of fancy operators and syntax requirements that prevent non-IT people from trying a little something out themselves. In these kind of situations, KRAN++ comes into play.

## Language
| Type                  | Token                     |
| --------------------- |-------------------------- |
| Assignment            | is                        |
| Add operator          | plus                      |
| Substract operator    | min                       |
| Multiply operator     | multiplied by             |
| Divide operator       | divided by                |
| If                    | when                      |
| Else                  | else                      |
| Equalilty operator    | is equal to               |
| Non-Equality operator | is not equal to           |
| Termination           | ]                         |
| Print                 | log                       |
| Larger than           | larger than               |
| Larger than or equal  | larger than or equal to   |
| Less than             | less than                 |
| Less than or equal    | less than or equal to     |

## Example
``` KRAN++
when 6 let 5 or 8 laq 6 {
	flush 8]
} else {
	flush 4]
}

val is 5 plus 4]				<!-- Comment --!>
next is val min 6]
prev is next div val]
res is prev mul val]

ok is next eq prev]				<!-- Ok contains wether next is equal to previous --!>
not_ok is next neq prev]

log 5 plus 5 plus next]			<!-- Print 5 + 5 + next --!>
```