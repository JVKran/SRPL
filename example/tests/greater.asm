	.cpu cortex-m0
	.text
	.align 2
	.global greater

greater:
	push 	{ lr }
	mov 	r2, #1
	cmp 	r0, r1
	bgt 	.L2
	movs	r2, #0
.L2:								@ Register r2 contains wether r0 is greater than r1.
end:
	movs	r0, r2                    	@ Move contents of r2 to r0 for returning.
	pop 	{ pc }