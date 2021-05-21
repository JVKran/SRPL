	.cpu cortex-m0
	.text
	.align 2
	.global fact

fact:
	push 	{ lr }
	movs	r1, #1					@ Register r1 contains 1.
	movs	r2, #2					@ Register r2 contains 2.
	movs	r3, #1
	@ Should for-loop be entered?
	cmp 	r0, #1
	ble 	end
loop:
	mul 	r1, r1, r2         		@ Register r1 contains result from multiplication of registers r1 and r2.
	add 	r2, r3                	@ Increment counter with stepsize.
	cmp 	r2, r0                	@ Compare counter with value to iterate towards.
	ble 	loop
end:
	movs	r0, r1                    	@ Move contents of r1 to r0 for returning.
	pop 	{ pc }