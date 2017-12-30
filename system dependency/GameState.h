// Templated classes for the gamestates, the objects responsible for managing the systems.

#pragma once

#include "System.h"
#include "utils.h"

#include <iostream>

template<class... OtherDependencies>
class _System;

template<class... OtherDependencies>
class System;

// Base case.
template<size_t K, class... OtherSystems>
class _GameState {
protected:
	_GameState() {}

	// This gets called when the system requested wasn't found.
	template<typename T>
	T* getSystem() {
		static_assert(is_system<T>::value, "That is not a system!");
		static_assert(!is_system<T>::value, "That system is not in the gamestate!");
	}

	template<typename BaseClass>
	void init(){}

	void update(unsigned int logicTime) {}

	template<typename T, typename BaseClass>
	void _init() {
		static_assert(is_system<T>::value, "That is not a system!");
		static_assert(!is_system<T>::value, "That system is not in the gamestate!");
	}

	// This gets called when the system requested wasn't found.
	template<typename T>
	constexpr bool hasSystem() const {
		static_assert(is_system<T>::value, "That is not a system!");
		return false;
	}

	// Container with all the system in the gamestate.
	_System<>* systems[K]; // Should it be done with a std::vector instead?
};

// Variadic recursive case.
template<size_t K, class S, class... OtherSystems>
class _GameState<K, S, OtherSystems...> : public _GameState<K + 1, OtherSystems...> {
protected:
	_GameState() {
		static_assert(is_system<S>::value, "That is not a system!");
		systems[K] = new S(); // What is a smart pointer?
	}

public:
	// Returns the specified system.
	template<typename T>
	T* getSystem() {
		return _GameState<K + 1, OtherSystems...>::getSystem<T>();
	}

	template<>
	S* getSystem() {
		return static_cast<S*>(systems[K]);
	}

	template<typename T>
	constexpr bool hasSystem() const {
		return _GameState<K + 1, OtherSystems...>::hasSystem<T>();
	}

	template<>
	constexpr bool hasSystem<S>() const {
		return true;
	}

	template<typename BaseClass>
	void init() {
		_init<S, BaseClass>();
		_GameState<K + 1, OtherSystems...>::init<BaseClass>();
	}

	template<typename T, typename BaseClass>
	void _init() {
		PartialSpecizlizationStruct<T, BaseClass>::_init(static_cast<BaseClass*>(this));
	}

	template<class T, class BaseClass>
	struct PartialSpecizlizationStruct {
		static void _init(BaseClass* gs) {
			gs->_GameState<K + 1, OtherSystems...>::_init<T, BaseClass>();
		}
	};

	template<typename BaseClass>
	struct PartialSpecizlizationStruct<S, BaseClass> {
		static void _init(BaseClass* gs) {
			S* mySystem = gs->getSystem<S>();

			if (!mySystem->was_initialized) {
				std::cout << "Initializing system..." << std::endl;
				mySystem->_init<BaseClass>(gs);
				mySystem->init();
			}

			else
				std::cout << "System already initialized." << std::endl;
		}
	};

	void update(unsigned int logicTime) {
		// TODO.
	}
};

// Interface to the programmer.
template<class... OtherSystems>
class GameState final : public _GameState<0, OtherSystems...> {
public:
	// Initializes all the systems in order.
	void init() {
		std::cout << "Initializing gamestate..." << std::endl;
		_GameState<0, OtherSystems...>::init<GameState>();
		std::cout << "Gamestate initialized!" << std::endl;
	}

	// Initializes a particular system and all its dependencies.
	template<typename T>
	void _init() {
		_GameState<0, OtherSystems...>::_init<T, GameState>();
	}

	void update(unsigned int logicTime) {
		_GameState<0, OtherSystems...>::update<T>(logicTime);
	}
};
