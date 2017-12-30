// Prototype for the system and gamestate infrastructure, which could help
// implement parallelism.
// It requires the BOOST libraries for template magic.

#include "GameState.h"
#include "System.h"

#include <iostream>

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
};

class SystemB : public System<SystemC> {
public:
	void init() {
		std::cout << "System B was initialized successfully." << std::endl;
	}

};

class SystemC : public System<> {
public:
	void init() {
		std::cout << "System C was initialized successfully." << std::endl;
	}

};

class SystemD : public System<SystemA, SystemB> {
public:
	void init() {
		std::cout << "System D was initialized successfully." << std::endl;
	}

};

class SystemE : public System<> {
public:
	void init() {
		std::cout << "System E was initialized successfully." << std::endl;
	}

};

int main() {
	GameState<SystemA, SystemB, SystemC, SystemD, SystemE> gs;
	gs.init();
	return 0;
}