	.cpu cortex-m0
	.text
	.align 2
	.global less_equal

less_equal:
	push 	{ lr }
	lsr 	r2, r0, #31
	asr 	r3, r1, #31
	cmp 	r1, r0
	adc 	r2, r2, r3		        @ Register r2 contains wether r0 is less than or equal to r1.
end:
	movs	r0, r2                    	@ Move contents of r2 to r0 for returning.
	pop 	{ pc }