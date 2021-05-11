#include "bmptk.h"

void delay(const uint16_t delay_ms){
	for(int i = 0; i < delay_ms * 1000; ++i){
		__ASM("nop");
	}	
}

int main( void ){   
   WDT->WDT_MR = WDT_MR_WDDIS;          // Kill watchdog
   PIOB->PIO_OER = 0x1U << 27;          // Enable output
   
   for(;;){
        PIOB->PIO_SODR = 0x01 << 27;    // Set pin
        delay(250);
        PIOB->PIO_CODR = 0x01 << 27;    // Clear pin
        delay(250);
    }
}
