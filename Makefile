SOURCES :=
HEADERS :=
SEARCH  := 

TARGET            ?= arduino_due
SERIAL_PORT       ?= COM2
RUN_TERMINAL      ?=					# Don't run terminal 

RELATIVE          ?= ../ATP
BMPTK             := $(RELATIVE)/bmptk

include           $(BMPTK)/makefile.inc