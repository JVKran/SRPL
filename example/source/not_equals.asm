	.cpu cortex-m0
	.text
	.align 2
	.global not_equals

not_equals:
	push 	{r4, r5, r6, r7, lr}
	sub 	r2, r1, r0
	sub 	r3, r2, #1
	sbc 	r2, r2, r3
end:
	movs	r0, r2
	pop 	{r4, r5, r6, r7, pc}
