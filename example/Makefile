SOURCES 		:= $(wildcard */*.asm) srpl_tests.c
HEADERS			:= srpl_tests.h

TARGET          ?= arduino_due
SERIAL_PORT     ?= COM2
RUN_TERMINAL    ?= # Don't run terminal 

RELATIVE        ?= ../../ATP
BMPTK           := $(RELATIVE)/bmptk

compile:
	python ../srpl.py

include         $(BMPTK)/makefile.inc