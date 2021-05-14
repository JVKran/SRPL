	.cpu cortex-m0
	.text
	.align 2
	.global if_test

if_test:
	push 	{ lr }
	movs	r1, #3
	sub 	r3, r1, r0
	neg 	r2, r3
	adc 	r2, r2, r3		         @ Register r2 contains wether r0 and r1 are equal.
	cmp 	r2, #1
	bne 	.L2
	movs	r3, #1
	b   	.L4 
.L2:
	movs	r3, #0
.L4:
end:
	movs	r0, r3
	pop 	{ pc }