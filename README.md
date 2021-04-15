# KRAN++

## Language
| Type                  | Token     |
| --------------------- |---------- |
| Assignment            | is        |
| Add operator          | plus      |
| Substract operator    | min       |
| Multiply operator     | mul       |
| Divide operator       | div       |
| If                    | when      |
| Else                  | else      |
| Equalilty operator    | eq        |
| Non-Equality operator | neq       |
| Termination           | ]         |
| Print                 | log       |

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