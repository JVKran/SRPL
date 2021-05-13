	.cpu cortex-m0
	.text
	.align 2
	.global greater_equal

greater_equal:
	push 	{r4, r5, r6, r7, lr}
	asr 	r2, r0, #31
	lsr 	r3, r1, #31
	cmp 	r0, r1
	adc 	r2, r2, r3
end:
	movs	r0, r2
	pop 	{r4, r5, r6, r7, pc}
