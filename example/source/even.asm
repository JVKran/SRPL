	.cpu cortex-m0
	.text
	.align 2
	.global even

even:
	push 	{ lr }
	pop 	{ pc }