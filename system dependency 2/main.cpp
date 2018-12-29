#include "PrototypeGameWorld.h"

int main()
{
	PrototypeGameWorld world;
	world.init();
	for (int i = 0; i < 100; i++) world.run();
	return 0;
}