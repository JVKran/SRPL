	.cpu cortex-m0
	.text
	.align 2
	.global even

even:
	push 	{r4, r5, r6, r7, lr}
	movs	r1, #0
	sub 	r3, r1, r0
	neg 	r2, r3
	adc 	r2, r2, r3
	cmp 	r2, #1
	bne 	.L2
	movs	r3, #1
	b	end 
.L2:
	movs	r3, #1
	sub 	r0, r3
	bl  	odd
	movs	r3, r0
end:
	movs	r0, r3
	pop 	{r4, r5, r6, r7, pc}
