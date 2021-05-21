	.cpu cortex-m0
	.text
	.align 2
	.global if_test

if_test:
	push 	{ lr }
	movs	r1, #3					@ Register r1 contains 3.
	sub 	r3, r1, r0
	neg 	r2, r3
	adc 	r2, r2, r3		        @ Register r2 contains wether r0 and r1 are equal.
	cmp 	r2, #1             		@ Register r2 contains wether condition is met.
	bne 	.L2            			@ Branch to .L2 if condition isn't met.
	movs	r3, #1					@ Register r3 contains 1.
	b   	.L4             		@ Branch to end of if/else-statement.
.L2:
	movs	r3, #0					@ Register r3 contains 0.
.L4:
end:
	movs	r0, r3                    @ Move contents of r3 to r0 for returning.
	pop 	{ pc }