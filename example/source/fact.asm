	.cpu cortex-m0
	.text
	.align 2
	.global fact

fact:
	push 	{ lr }
	movs	r1, #1					@ Register r1 contains 1.
	pop 	{ pc }