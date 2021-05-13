	.cpu cortex-m0
	.text
	.align 2
	.global multiply

multiply:
	push 	{r4, r5, r6, r7, lr}
	mul	r0, r0, r1
end:
	movs	r0, r0
	pop 	{r4, r5, r6, r7, pc}
