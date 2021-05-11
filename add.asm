add(int, int, int):
	push 	{r4, r5, r6, lr}
	adds 	r0, r0, r1
	adds 	r0, r0, r2
	pop 	{r4, r5, r6, pc}
