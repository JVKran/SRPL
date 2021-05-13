#include <stdint.h>
#include <stdbool.h>

#include "bmptk.h"
#include "srpl_tests.h"

#define LED_GPIO    27

void delay(const uint16_t delay_ms){
	for(int i = 0; i < delay_ms * 1000; ++i){
		__ASM("nop");
	}	
}

int main( void ){   
    WDT->WDT_MR = WDT_MR_WDDIS;                 // Kill watchdog
    PIOB->PIO_OER = 0x1U << LED_GPIO;           // Enable output

    bool all_correct = run_tests();
    uint16_t duration = all_correct ? 100 : 1000;

    for(;;){
        PIOB->PIO_SODR = 0x01 << LED_GPIO;      // Set pin
        delay(duration);
        PIOB->PIO_CODR = 0x01 << LED_GPIO;      // Clear pin
        delay(duration);
    }
}
