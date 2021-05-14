	.cpu cortex-m0
	.text
	.align 2
	.global greater_equal

greater_equal:
	push 	{ lr }
	pop 	{ pc }