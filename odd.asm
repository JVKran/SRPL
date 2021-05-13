        .cpu cortex-m0
        .text
        .align 2
        .global odd

odd:
        push    {r4, r5, r6, lr}
        sub     r0, r0, r0
        neg     r1, r0
        adc     r1, r1, r0
        cmp     r1, #1
        bne     .L2
        movs    r0, #0
        b       end
.L2:
        movs    r0, r0
        movs    r3, #1
        sub     r0, r0, #1
        bl      even
end:
        pop     {r4, r5, r6, pc}

