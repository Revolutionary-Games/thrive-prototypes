// Templated classes for the systems, the objects that have all the functionality in the game.

#pragma once

#include "utils.h"

// This empty class is used to mark dependencies from one system to another.
template<class S>
class _SystemDependency {};

// Base case.
template<class... OtherDependencies>
class _System {
public:
	// The base system doesn't depend on anything.
	class Dependencies {};
};

// Variadic recursive case.
template<class D, class... OtherDependencies>
class _System<D, OtherDependencies...> : public _System<OtherDependencies...> {
public:
	_System<D, OtherDependencies...>() {
		static_assert(is_system<D>::value, "That is not a system!");

		// Doesn't actually display that message but it triggers a compile error, which is good enough...
		static_assert(!depends_on<D, _System<D, OtherDependencies...>>::value, "Mutual system dependency detected!");
	}

	// This class inherits all the dependencies this system has.
	class Dependencies : public _SystemDependency<D>,
						 public D::Dependencies,
						 public _System<OtherDependencies...>::Dependencies {};
};

// Interface to the programmer.
template<class... OtherDependencies>
class System : public _System<OtherDependencies...> {
public:
	class Dependencies : public _System<OtherDependencies...>::Dependencies {};
};
