        .cpu cortex-m0
        .text
        .align 2
        .global equals

equals:
        push    {r4, r5, r6, lr}
        movs    r0, r0
        movs    r0, r1
        sub     r0, r1, r0
        neg     r0, r0
        adc     r0, r0, r0
        movs    r0, r0
end:
        pop     {r4, r5, r6, pc}