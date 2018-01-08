// Templated classes for the gamestates, the objects responsible for managing the systems.

#pragma once

#include "System.h"

#include <iostream>
#include <thread>
#include <shared_mutex>
#include <tuple>
#include <vector>

// Interface to the programmer.
template<class... Systems>
class GameState final {
private:
	// A tuple which stores all the systems.
	std::tuple<Systems...> systems;
	using NumberOfSystems = std::tuple_size<decltype(systems)>;

	// Auxiliary structure that holds information about each system.
	struct SystemData {
		// This mutex is used 
		std::shared_timed_mutex systemMutex;

		// The numbers of the systems that have to run before this system.
		std::vector<size_t> dependencies;

		// Flag that indicates whether the system was initialized or not.
		bool was_initialized = false;

		// Lambda interfaces to the system's methods.
		std::function<void(void)> initializeSystem;
		std::function<void(unsigned int)> updateSystem;
	};

	// An array with all the systems's data.
	SystemData systemInformation[NumberOfSystems::value];

	// Locks all the mutexes before an update cycle.
	void lockAllMutexes() {
		for (size_t i = 0; i < NumberOfSystems::value; i++)
			systemInformation[i].systemMutex.lock();
	}

	// Updates a system (if it wasn't previously initialized), and all of its dependencies if needed.
	void initializeSystem(size_t systemNumber) {
		SystemData& systemData = systemInformation[systemNumber];

		// Checking that the system wasn't already initialized.
		if(!systemData.was_initialized) {
			// Initializing all the dependencies first.
			for (const size_t systemDependency : systemData.dependencies)
				initializeSystem(systemDependency);

			// Initializing the system itself.
			systemData.initializeSystem();

			// Setting the flag to avoid double initialization of the systems.
			systemData.was_initialized = true;
		}
	}

	// Updates a system, and manages synchronization.
	void updateSystem(size_t systemNumber, unsigned int logicTime) {
		SystemData& systemData = systemInformation[systemNumber];

		// Waiting for all of the dependencies to finish.
		for (const size_t systemDependency : systemData.dependencies) {
			systemInformation[systemDependency].systemMutex.lock_shared();
		}

		// Updating the system.
		systemData.updateSystem(logicTime);

		// Unlocking the mutex so that other systems that depend on this system can update.
		systemData.systemMutex.unlock();

		// Freeing the locks.
		for (const size_t systemDependency : systemData.dependencies) {
			systemInformation[systemDependency].systemMutex.unlock_shared();
		}
	}

	// Auxiliary structs to translate system numbers to system types because
	// using just decltype on tuples breaks the compiler lmao.

	// Empty base struct.
	template<size_t K, size_t SystemNumber, class... OtherSystems>
	struct _numberToSystemTypeTranslator{};

	// Struct with actually useful information.
	template<size_t SystemNumber, class S, class... OtherSystems>
	struct _numberToSystemTypeTranslator<SystemNumber, SystemNumber, S, OtherSystems...> {
		using SystemType = S;
	};

	// Recursive template specialization.
	template<size_t K, size_t SystemNumber, class S, class... OtherSystems>
	struct _numberToSystemTypeTranslator<K, SystemNumber, S, OtherSystems...> : public _numberToSystemTypeTranslator<K + 1, SystemNumber, OtherSystems...> {};

	// Pretty interface
	template<size_t SystemNumber>
	using numberToSystemTypeTranslator = _numberToSystemTypeTranslator<0, SystemNumber, Systems...>;

	// Generates all the dependency data.
	// Due to partial specialization of functions not being available
	// (and my unwillingness to create a struct to hack around it)
	// the system number and potential dependency are packed in a singular parameter.
	template<size_t N>
	void generateSystemDependencies() {
		// Unpacking the parameters
		constexpr size_t systemNumber = N % NumberOfSystems::value;
		constexpr size_t potentialDependency = N / NumberOfSystems::value;

		// If potentialDependency is actually a dependency.
		if (depends_on<numberToSystemTypeTranslator<systemNumber>::SystemType, numberToSystemTypeTranslator<potentialDependency>::SystemType>::value)
			// Add it to the dependency list.
			systemInformation[systemNumber].dependencies.push_back(potentialDependency);

		// Doing the next check.
		generateSystemDependencies<N + 1>();
	}

	// Empty function for the final recursive call.
	template<>
	void generateSystemDependencies<NumberOfSystems::value * NumberOfSystems::value>() {}

	// Generates the lambda interfaces that the system data has.
	template<size_t SystemNumber>
	void generateSystemFunctions() {
		SystemData& systemData = systemInformation[SystemNumber];
		auto& systemToCall = std::get<SystemNumber>(systems);

		// Getting the init method.
		systemData.initializeSystem = [&systemToCall]() {
			systemToCall.init();
		};

		// Getting the update method.
		systemData.updateSystem = [&systemToCall](unsigned int logicTime) {
			systemToCall.update(logicTime);
		};

		// Generating the next system.
		generateSystemFunctions<SystemNumber + 1>();
	}

	// Empty function for the final recursive call.
	template<>
	void generateSystemFunctions<NumberOfSystems::value>() {}

public:
	GameState() {
		generateSystemDependencies<0>();
		generateSystemFunctions<0>();
	}

	// Initializes all the systems in order.
	void init() {
		std::cout << "Initializing gamestate..." << std::endl;

		for (size_t i = 0; i < NumberOfSystems::value; i++)
			initializeSystem(i);

		std::cout << "Gamestate initialized!" << std::endl;
	}

	// Updates all the systems in order.
	void update(unsigned int logicTime) {
		std::cout << "Updating systems..." << std::endl;

		// Locking all the threads to be later unlocked when the systems update.
		lockAllMutexes();

		std::vector<std::thread> systemThreads;

		// Spawning all the update threads. It should probably be done in a more efficient way.
		for (size_t i = 0; i < NumberOfSystems::value; i++)
			systemThreads.emplace(systemThreads.end(), &GameState::updateSystem, this, i, logicTime);

		// Waiting for all the systems to finish.
		for (auto& systemThread : systemThreads)
			systemThread.join();

		std::cout << std::endl << "Systems updated!" << std::endl;
	}
};
