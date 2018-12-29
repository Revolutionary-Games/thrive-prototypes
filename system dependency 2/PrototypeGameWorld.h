#pragma once

#include "BaseWorld.h"

class PrototypeGameWorld : public BaseWorld
{
public:
	void init();

private:
	unsigned int planetsDestroyed = 0;
};
