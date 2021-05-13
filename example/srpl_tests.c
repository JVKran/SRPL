#include "srpl_tests.h"

bool and_test_desired(uint8_t a){
    return a > 50 && a <= 150;
}

bool or_test_desired(uint8_t a){
    return a >= 150 || a < 50;
}

bool run_tests(){
    bool all_correct = true;
    all_correct &= (summy(34) == 595);
    for(uint_fast8_t i = 0; i < 200; i++){
        all_correct &= (even(i) == (i % 2 == 0));
        all_correct &= (odd(i) == i % 2);
        all_correct &= equals(i, i);
        all_correct &= (not_equals(i, 200 - i) == (i != (200 - i)));
        all_correct &= (if_test(i) == (i == 3));
        all_correct &= (less(i, 200 - i) == (i < (200 - i)));
        all_correct &= (less_equal(i, 200 - i) == (i <= (200 - i)));
        all_correct &= (greater(i, 200 - i) == (i > (200 - i)));
        all_correct &= (greater_equal(i, 200 - i) == (i >= (200 - i)));
        all_correct &= (and_test(i) == and_test_desired(i));
        all_correct &= (or_test(i) == or_test_desired(i));
        all_correct &= (divide(i, (200 - i) + 1) == i / ((200 - i) + 1));
        all_correct &= (multiply(i, i) == i * i);
    }
    return all_correct;
}
