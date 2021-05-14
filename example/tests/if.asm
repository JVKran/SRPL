	.cpu cortex-m0
	.text
	.align 2
	.global if_test

if_test:
	push 	{ lr }
	pop 	{ pc }