#include "PrototypeGameWorld.h"

#include <iostream>

void PrototypeGameWorld::init()
{
	// A system.
	TaskInformation system1;
	system1.name = "system1";
	system1.task = []() { std::cout << "Running system 1!" << std::endl; };
	taskManager.addTask(system1);

	// Another system.
	TaskInformation system2;
	system2.name = "system2";
	system2.task = []() { std::cout << "Running system 2!" << std::endl; };
	taskManager.addTask(system2);

	// A system that depends on the first system.
	TaskInformation system3;
	system3.name = "system3";
	system3.task = []() { std::cout << "Running system 3!" << std::endl; };
	system3.precedingTasks = { "system1" };
	taskManager.addTask(system3);

	// A system that depends on the first 2 systems.
	TaskInformation system4;
	system4.name = "system4";
	system4.task = []() { std::cout << "Running system 4!" << std::endl; };
	system4.precedingTasks = { "system1", "system2" };
	taskManager.addTask(system4);

	// A system that modifies a variable.
	TaskInformation system5;
	system5.name = "system5";
	system5.task = [&]()
	{
		std::cout << "Running system 5! Destroying a planet!" << std::endl;
		planetsDestroyed++;
	};
	taskManager.addTask(system5);

	// A system that reads said variable.
	TaskInformation system6;
	system6.name = "system6";
	system6.task = [&]() { std::cout << "Running system 6! There are " << planetsDestroyed << " destroyed planets!" << std::endl;};
	system6.precedingTasks = { "system5" };
	taskManager.addTask(system6);

	// Calling the parent world to add the systems it might need.
	BaseWorld::init();
}
