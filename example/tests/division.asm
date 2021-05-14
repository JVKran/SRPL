	.cpu cortex-m0
	.text
	.align 2
	.global divide

divide:
	push 	{ lr }
	pop 	{ pc }