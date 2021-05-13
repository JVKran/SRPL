	.cpu cortex-m0
	.text
	.align 2
	.global divide

divide:
	push 	{r4, r5, r6, r7, lr}
	push	 {r0, r1}
	mov 	r0, r0
	mov 	r1, r1
	bl  	__aeabi_idiv
	mov 	r2, r0
	pop 	 {r0, r1}
end:
	movs	r0, r2
	pop 	{r4, r5, r6, r7, pc}
