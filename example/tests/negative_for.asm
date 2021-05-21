	.cpu cortex-m0
	.text
	.align 2
	.global neg_for

neg_for:
	push 	{ r4, lr }
	movs	r1, #1					@ Register r1 contains 1.
	movs	r2, #0					@ Register r2 contains 0.
	movs	r3, #0					@ Register r3 contains 0.
	movs	r4, #2					@ Register r4 contains 2.
	sub 	r3, r4         			@ Register r3 contains result from substraction of registers r3 and r4.
	@ Should for-loop be entered?
	cmp 	r2, #0
	bgt 	end
loop:
	add 	r1, r0         			@ Register r1 contains result from addition of registers r1 and r0.
	add 	r0, r3                	@ Increment counter with stepsize.
	cmp 	r0, r2                	@ Compare counter with value to iterate towards.
	bge 	loop
end:
	movs	r0, r1                    	@ Move contents of r1 to r0 for returning.
	pop 	{ r4, pc }