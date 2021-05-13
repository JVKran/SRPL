	.cpu cortex-m0
	.text
	.align 2
	.global less

less:
	push 	{r4, r5, r6, lr}
	mov 	r2, #1
	cmp 	r0, r1
	blt 	.L2
	movs	r2, #0
.L2:
end:
	movs	r0, r2
	pop 	{r4, r5, r6, pc}
