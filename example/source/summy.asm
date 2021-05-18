	.cpu cortex-m0
	.text
	.align 2
	.global summy

summy:
	push 	{ r4, lr }
	movs	r1, #0					@ Register r1 contains 0.
loop:
	movs	r2, #1					@ Register r2 contains 1.
	asr 	r3, r0, #31
	lsr 	r4, r2, #31
	cmp 	r0, r2
	adc 	r3, r3, r4		        @ Register r3 contains wether r0 is greater than or equal to r2.
	add 	r1, r0         			@ Register r1 contains result from addition of registers r1 and r0.
	movs	r4, #1					@ Register r4 contains 1.
	sub 	r0, r4         			@ Register r0 contains result from substraction of registers r0 and r4.
	cmp 	r3, #1            		@ Register r3 contains wether condition is met or not.
	beq 	loop            		@ Branch to loop when condition is met.
end:
	movs	r0, r1                    	@ Move contents of r1 to r0 for returning.
	pop 	{ r4, pc }