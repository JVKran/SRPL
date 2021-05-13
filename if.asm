        .cpu cortex-m0
        .text
        .align 2
        .global if_test

if_test:
        push    {r4, r5, r6, lr}
        movs    r0, r0
        movs    r1, #3
        sub     r0, r1, r0
        neg     r2, r0
        adc     r2, r2, r0
        cmp     r2, #1
        bne     .L2
        movs    r3, #1
        b       end
.L2:
        movs    r3, #0
        movs    r0, r3
        movs    r0, r3
end:
        movs    r0, r3
        pop     {r4, r5, r6, pc}