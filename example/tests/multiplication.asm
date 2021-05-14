	.cpu cortex-m0
	.text
	.align 2
	.global multiply

multiply:
	push 	{ lr }
	mul 	r0, r0, r1
end:
	movs	r0, r0
	pop 	{ pc }