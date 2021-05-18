	.cpu cortex-m0
	.text
	.align 2
	.global multiply

multiply:
	push 	{ lr }
	mul 	r0, r0, r1         		@ Register r0 contains result from multiplication of registers r0 and r1.
end:
	pop 	{ pc }