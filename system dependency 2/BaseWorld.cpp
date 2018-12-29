#include "BaseWorld.h"

void BaseWorld::init()
{
	taskManager.generateDependencyGraph();
}

void BaseWorld::run()
{
	taskManager.run();
}
