#ifndef __SRPL_TESTS_H
#define __SRPL_TESTS_H

#include <stdint.h>
#include <stdbool.h>

extern bool even(uint8_t);
extern bool odd(uint8_t);
extern bool equals(uint8_t, uint8_t);
extern bool if_test(uint8_t);
extern int16_t summy(uint8_t);
extern bool less(uint8_t, uint8_t);
extern bool greater(uint8_t, uint8_t);
extern bool less_equal(uint8_t, uint8_t);
extern bool greater_equal(uint8_t, uint8_t);
extern bool and_test(uint8_t);
extern bool or_test(uint8_t);
extern bool not_equals(uint8_t, uint8_t);
extern uint8_t divide(uint8_t, uint8_t);
extern uint16_t multiply(uint8_t, uint8_t);
extern int fact(int);
extern int neg_for(int);

bool and_test_desired(uint8_t);
bool or_test_desired(uint8_t);
int negative_for(int);

bool run_tests();

#endif //__SRPL_TESTS_H