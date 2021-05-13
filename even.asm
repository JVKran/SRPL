        .cpu cortex-m0
        .text
        .align 2
        .global even

even:
        push    {r4, lr}
        movs    r3, r0
        movs    r0, #1
        cmp     r3, #0
        bne     .L4
.L2:
        pop     {r4, pc}
.L4:
        sub     r0, r3, #1
        bl      odd
        b       .L2