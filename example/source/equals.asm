	.cpu cortex-m0
	.text
	.align 2
	.global equals

equals:
	push 	{r4, r5, r6, lr}
	sub 	r3, r1, r0
	neg 	r2, r3
	adc 	r2, r2, r3
end:
	movs	r0, r2
	pop 	{r4, r5, r6, pc}
