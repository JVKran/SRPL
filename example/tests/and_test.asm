	.cpu cortex-m0
	.text
	.align 2
	.global and_test

and_test:
	push 	{r4, r5, r6, r7, lr}
	movs	r1, #50
	mov 	r2, #1
	cmp 	r0, r1
	bgt 	.L2
	movs	r2, #0
.L2:
	movs	r3, #150
	lsr 	r4, r0, #31
	asr 	r5, r3, #31
	cmp 	r3, r0
	adc 	r4, r4, r5
	asr 	r6, r2, #31
	sub 	r5, r6, r2
	asr 	r6, r4, #31
	sub 	r7, r6, r4
	and 	r5, r5, r7
	lsr 	r5, r5, #31
end:
	movs	r0, r5
	pop 	{r4, r5, r6, r7, pc}
