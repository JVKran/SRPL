        .cpu cortex-m0
        .text
        .align 2
        .global if_test

if_test:
        push    {r4, r5, r6, lr}
        movs    r1, #3
        sub     r3, r1, r0
        neg     r2, r3
        adc     r2, r2, r3
        cmp     r2, #1
        bne     .L2
        movs    r4, #1
        b       end
.L2:
        movs    r4, #0
end:
        movs    r0, r4
        pop     {r4, r5, r6, pc}