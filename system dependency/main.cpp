// Prototype for the system and gamestate infrastructure, which could help
// implement parallelism.
// It requires the BOOST libraries for template magic.

#include "GameState.h"
#include "System.h"

#include <iostream>
#include <chrono>
#include <thread>

// The minimum time (in milliseconds) between character prints in each system.
#define WAITING_TIME 100

// The number of update cycles in the test simulation.
#define UPDATE_CYCLE_NUMBER 10

// The number of characters printed on each update cycle.
#define NUMBER_OF_CHARACTERS 100

class SystemA;
class SystemB;
class SystemC;
class SystemD;
class SystemE;

class SystemA : public System<SystemB> {
public:
	void init() {
		std::cout << "System A was initialized successfully." << std::endl;
	}

	void update(unsigned int logicTime) {
		for (unsigned int i = 0; i < logicTime; i++) {
			std::cout << "A";
			std::this_thread::sleep_for(std::chrono::milliseconds(WAITING_TIME));
		}
	}
};

class SystemB : public System<SystemC> {
public:
	void init() {
		std::cout << "System B was initialized successfully." << std::endl;
	}

	void update(unsigned int logicTime) {
		for (unsigned int i = 0; i < logicTime; i++) {
			std::cout << "B";
			std::this_thread::sleep_for(std::chrono::milliseconds(WAITING_TIME));
		}
	}

};

class SystemC : public System<> {
public:
	void init() {
		std::cout << "System C was initialized successfully." << std::endl;
	}

	void update(unsigned int logicTime) {
		for (unsigned int i = 0; i < logicTime; i++) {
			std::cout << "C";
			std::this_thread::sleep_for(std::chrono::milliseconds(WAITING_TIME));
		}
	}

};

class SystemD : public System<SystemA, SystemB> {
public:
	void init() {
		std::cout << "System D was initialized successfully." << std::endl;
	}

	void update(unsigned int logicTime) {
		for (unsigned int i = 0; i < logicTime; i++) {
			std::cout << "D";
			std::this_thread::sleep_for(std::chrono::milliseconds(WAITING_TIME));
		}
	}

};

class SystemE : public System<> {
public:
	void init() {
		std::cout << "System E was initialized successfully." << std::endl;
	}

	void update(unsigned int logicTime) {
		for (unsigned int i = 0; i < logicTime; i++) {
			std::cout << "E";
			std::this_thread::sleep_for(std::chrono::milliseconds(WAITING_TIME));
		}
	}

};

int main() {
	GameState<SystemA, SystemB, SystemC, SystemD, SystemE> gs;
	gs.init();

	for(int i = 0; i < UPDATE_CYCLE_NUMBER; i++)
		gs.update(NUMBER_OF_CHARACTERS);

	return 0;
}