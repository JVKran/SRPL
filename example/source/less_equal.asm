	.cpu cortex-m0
	.text
	.align 2
	.global less_equal

less_equal:
	push 	{r4, r5, r6, lr}
	lsr 	r2, r0, #31
	asr 	r3, r1, #31
	cmp 	r1, r0
	adc 	r2, r2, r3
end:
	movs	r0, r2
	pop 	{r4, r5, r6, pc}
