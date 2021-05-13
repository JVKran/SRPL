	.cpu cortex-m0
	.text
	.align 2
	.global or_test

or_test:
	push 	{r4, r5, r6, r7, lr}
	movs	r1, #150
	asr 	r2, r0, #31
	lsr 	r3, r1, #31
	cmp 	r0, r1
	adc 	r2, r2, r3
	movs	r3, #50
	mov 	r4, #1
	cmp 	r0, r3
	blt 	.L2
	movs	r4, #0
.L2:
	asr 	r6, r2, #31
	sub 	r5, r6, r2
	asr 	r6, r4, #31
	sub 	r7, r6, r4
	orr 	r5, r5, r7
	lsr 	r5, r5, #31
end:
	movs	r0, r5
	pop 	{r4, r5, r6, r7, pc}
