	.cpu cortex-m0
	.text
	.align 2
	.global odd

odd:
	push 	{r4, r5, r6, lr}
	movs	r1, #0
	sub 	r3, r1, r0
	neg 	r2, r3
	adc 	r2, r2, r3
	cmp 	r2, #1
	bne 	.L2
	movs	r4, #0
	b	end 
.L2:
	movs	r4, #1
	sub 	r0, r4
	bl  	even
	movs	r4, r0
end:
	movs	r0, r4
	pop 	{r4, r5, r6, pc}
