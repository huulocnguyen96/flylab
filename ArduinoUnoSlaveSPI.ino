/*
  This file details the arduino code to turn the arduino uno into a slave and setup an interupt. 
  The code to set up the RPi will be in a separate file
  This has been sourced from https://roboticsbackend.com/raspberry-pi-master-arduino-uno-slave-spi-communication-with-wiringpi/
*/ 


#include <SPI.h>

void setup() {
  // have to send on master in, *slave out*
  pinMode(MISO, OUTPUT);

  // turn on SPI in slave mode
  SPCR |= _BV(SPE);

  // turn on interrupts
  SPI.attachInterrupt();
}

// SPI interrupt routine
ISR (SPI_STC_vect)
{
  byte c = SPDR;

  SPDR = c+10;
}  // end of interrupt service routine (ISR) for SPI

void loop () { }
