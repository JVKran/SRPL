	.cpu cortex-m0
	.text
	.align 2
	.global greater_equal

greater_equal:
	push 	{ lr }
	asr 	r2, r0, #31
	lsr 	r3, r1, #31
	cmp 	r0, r1
	adc 	r2, r2, r3		        @ Register r2 contains wether r0 is greater than or equal to r1.
end:
	movs	r0, r2                    	@ Move contents of r2 to r0 for returning.
	pop 	{ pc }