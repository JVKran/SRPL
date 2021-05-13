#include "bmptk.h"
#include <stdint.h>
#include <stdbool.h>

#define LED_GPIO    27

extern int even(int a);
extern int odd(int b);
extern bool equals(int a, int b);
extern bool if_test(int a);

void delay(const uint16_t delay_ms){
	for(int i = 0; i < delay_ms * 1000; ++i){
		__ASM("nop");
	}	
}

int main( void ){   
    WDT->WDT_MR = WDT_MR_WDDIS;                 // Kill watchdog
    PIOB->PIO_OER = 0x1U << LED_GPIO;           // Enable output

    bool all_correct = true;
    for(uint8_t i = 0; i < 200; i++){
        all_correct &= (even(i) == (i % 2 == 0));
        all_correct &= (odd(i) == i % 2);
        all_correct &= equals(i, i);
        all_correct &= (if_test(i) == (i == 3));
    }

    uint16_t duration = all_correct ? 100 : 1000;

    for(;;){
        PIOB->PIO_SODR = 0x01 << LED_GPIO;      // Set pin
        delay(duration);
        PIOB->PIO_CODR = 0x01 << LED_GPIO;      // Clear pin
        delay(duration);
    }
}
