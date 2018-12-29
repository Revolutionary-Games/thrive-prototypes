#pragma once

#include "TaskManager.h"

class BaseWorld
{
public:
	void init();
	void run();

protected:
	TaskManager taskManager;
};
