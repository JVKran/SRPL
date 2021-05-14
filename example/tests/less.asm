	.cpu cortex-m0
	.text
	.align 2
	.global less

less:
	push 	{ lr }
	mov 	r2, #1
	cmp 	r0, r1
	blt 	.L2
	movs	r2, #0
.L2:					@Register r2 contains wether r0 is less than r1.
end:
	movs	r0, r2
	pop 	{ pc }