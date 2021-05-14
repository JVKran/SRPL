	.cpu cortex-m0
	.text
	.align 2
	.global odd

odd:
	push 	{ lr }
	pop 	{ pc }