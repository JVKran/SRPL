	.cpu cortex-m0
	.text
	.align 2
	.global summy

summy:
	push 	{r4, r5, r6, r7, lr}
	movs	r1, #0
loop:
	movs	r2, #1
	asr 	r3, r0, #31
	lsr 	r4, r2, #31
	cmp 	r0, r2
	adc 	r3, r3, r4
	cmp 	r3, #1
	bne 	end
	add 	r1, r0
	movs	r4, #1
	sub 	r0, r4
	b    	loop
end:
	movs	r0, r1
	pop 	{r4, r5, r6, r7, pc}
