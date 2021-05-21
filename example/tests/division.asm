	.cpu cortex-m0
	.text
	.align 2
	.global divide

divide:
	push 	{ lr }
	push	{r0, r1}				@ Push original values to stack.
	mov 	r0, r0					@ Move registers to divide to r0 and r1.
	mov 	r1, r1
	bl  	__aeabi_idiv
	mov 	r2, r0					@ Store result of division in r2.
	pop 	{r0, r1}				@ Restore original values of r0 and r1.
end:
	movs	r0, r2                    @ Move contents of r2 to r0 for returning.
	pop 	{ pc }