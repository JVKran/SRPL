	.cpu cortex-m0
	.text
	.align 2
	.global equals

equals:
	push 	{ lr }
	sub 	r3, r1, r0
	neg 	r2, r3
	adc 	r2, r2, r3		        @ Register r2 contains wether r0 and r1 are equal.
end:
	movs	r0, r2                    	@ Move contents of r2 to r0 for returning.
	pop 	{ pc }