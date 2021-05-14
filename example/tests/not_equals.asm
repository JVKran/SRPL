	.cpu cortex-m0
	.text
	.align 2
	.global not_equals

not_equals:
	push 	{ lr }
	sub 	r2, r1, r0
	sub 	r3, r2, #1
	sbc 	r2, r2, r3		@ Register r2 contains wether r0 and r1 are not equal.
end:
	movs	r0, r2
	pop 	{ pc }