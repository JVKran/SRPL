#include "bmptk.h"
#include <stdint.h>
#include <stdbool.h>

#define LED_GPIO    27

extern int even(int a);
extern int odd(int b);
extern bool equals(int a, int b);
extern bool if_test(int a);
extern int summy(int a);
extern bool less(int a, int b);
extern bool greater(int a, int b);
extern bool less_equal(int a, int b);
extern bool greater_equal(int a, int b);
extern bool and_test(int a);
extern bool or_test(int a);
extern bool not_equals(int a, int b);
extern int divide(int a, int b);
extern int multiply(int a, int b);

void delay(const uint16_t delay_ms){
	for(int i = 0; i < delay_ms * 1000; ++i){
		__ASM("nop");
	}	
}

bool and_test_desired(int a){
    return a > 50 && a <= 150;
}

bool or_test_desired(int a){
    return a >= 150 || a < 50;
}

int main( void ){   
    WDT->WDT_MR = WDT_MR_WDDIS;                 // Kill watchdog
    PIOB->PIO_OER = 0x1U << LED_GPIO;           // Enable output

    bool all_correct = true;
    all_correct &= (summy(34) == 595);
    for(uint8_t i = 0; i < 200; i++){
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

    uint16_t duration = all_correct ? 100 : 1000;

    for(;;){
        PIOB->PIO_SODR = 0x01 << LED_GPIO;      // Set pin
        delay(duration);
        PIOB->PIO_CODR = 0x01 << LED_GPIO;      // Clear pin
        delay(duration);
    }
}
