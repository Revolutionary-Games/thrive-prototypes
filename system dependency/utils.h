// File with miscelaneous template stuff.

#pragma once

#include "System.h"

#include <boost/type_traits.hpp>

template<class S>
class _SystemDependency;

template<class... OtherDependencies>
class _System;

// Checks if T is a system.
template <class T>
using is_system = std::is_base_of<_System<>, T>;

// Checks if S1 depends on S2.
template <class S1, class S2>
using depends_on = std::is_base_of<_SystemDependency<S2>, typename S1::Dependencies>;
