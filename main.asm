	.cpu cortex-m0
	.text
	.align 2
	.global add

add:
	push 	{r4, r5, r6, r7, lr}
	add 	r0, r1
end:
	movs	r0, r0
	movs	r2, #3
	movs	r3, #5
	bl  	add
	movs	r4, #4
	movs	r5, #5
	bl  	sum
end:
	pop 	{r4, r5, r6, r7, pc}
