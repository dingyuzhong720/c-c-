CC = gcc
CXX = g++
CFLAGS = -std=c11 -Wall -Wextra -Wpedantic -g3 -O0
CXXFLAGS = -std=c++17 -Wall -Wextra -Wpedantic -g3 -O0

.PHONY: all c cpp run-c run-cpp check
all: c cpp
c: build/fahrenheit-c
cpp: build/fahrenheit-cpp

build:
	mkdir -p build

build/fahrenheit-c: src/fahrenheit.c Makefile | build
	$(CC) $(CPPFLAGS) $(CFLAGS) $< -o $@ $(LDFLAGS) $(LDLIBS)

build/fahrenheit-cpp: src/fahrenheit.cpp Makefile | build
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $< -o $@ $(LDFLAGS) $(LDLIBS)

run-c: c
	./build/fahrenheit-c

run-cpp: cpp
	./build/fahrenheit-cpp

check: all
	python3 tests/verify.py build/fahrenheit-c build/fahrenheit-cpp
