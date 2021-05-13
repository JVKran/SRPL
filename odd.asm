	.cpu cortex-m0
	.text
	.align 2
	.global odd

odd:
        push    {r4, lr}
        movs    r3, r0
        movs    r0, #0
        cmp     r3, #0
        bne     .L8
.L6:
        pop     {r4, pc}
.L8:
        sub     r0, r3, #1
        bl      even
        b       .L6