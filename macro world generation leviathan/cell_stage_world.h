#pragma once

#include "Entities/GameWorld.h"
#include "Generated/StandardWorld.h"
#include "microbe_stage/membrane_system.h"
#include "microbe_stage/compound_cloud_system.h"
#include "microbe_stage/process_system.h"
#include "microbe_stage/species_component.h"
#include "microbe_stage/spawn_system.h"
#include "microbe_stage/agent_cloud_system.h"
#include "microbe_stage/compound_absorber_system.h"
#include "microbe_stage/microbe_camera_system.h"

// This would be defined in each system, and maybe with a similar idiom to the component and 
// system lists below.
#define COMPONENT_CONSTRUCTOR_PARAMETERS_ProcessorComponent
#define COMPONENT_CONSTRUCTOR_PARAMETERS_CompoundBagComponent
#define COMPONENT_CONSTRUCTOR_PARAMETERS_SpeciesComponent , const std::string &name
#define COMPONENT_CONSTRUCTOR_PARAMETERS_MembraneComponent
#define COMPONENT_CONSTRUCTOR_PARAMETERS_CompoundCloudComponent , CompoundId compoundid, float red, float green, float blue
#define COMPONENT_CONSTRUCTOR_PARAMETERS_AgentCloudComponent , CompoundId compoundid, float red, float green, float blue
#define COMPONENT_CONSTRUCTOR_PARAMETERS_SpawnedComponent , double newspawnradius
#define COMPONENT_CONSTRUCTOR_PARAMETERS_CompoundAbsorberComponent

#define COMPONENT_CONSTRUCTOR_ARGUMENTS_ProcessorComponent
#define COMPONENT_CONSTRUCTOR_ARGUMENTS_CompoundBagComponent
#define COMPONENT_CONSTRUCTOR_ARGUMENTS_SpeciesComponent , name
#define COMPONENT_CONSTRUCTOR_ARGUMENTS_MembraneComponent
#define COMPONENT_CONSTRUCTOR_ARGUMENTS_CompoundCloudComponent , compoundid, red, green, blue
#define COMPONENT_CONSTRUCTOR_ARGUMENTS_AgentCloudComponent , compoundid, red, green, blue
#define COMPONENT_CONSTRUCTOR_ARGUMENTS_SpawnedComponent , newspawnradius
#define COMPONENT_CONSTRUCTOR_ARGUMENTS_CompoundAbsorberComponent

// Insert your components here:
#define COMPONENT_LIST				\
C_(ProcessorComponent)				\
C_(CompoundBagComponent)			\
C_(SpeciesComponent)				\
C_(MembraneComponent)				\
C_(CompoundCloudComponent)			\
C_(AgentCloudComponent)				\
C_(SpawnedComponent)				\
C_(CompoundAbsorberComponent)

// Insert your components here:
#define SYSTEM_LIST					\
S_(MembraneSystem)					\
S_(SpawnSystem)						\
S_(AgentCloudSystem)				\
S_(CompoundAbsorberSystem)			\
S_(MicrobeCameraSystem)				\
S_(ProcessSystem)

// Auxiliary struct shamelessly ripped off from a Stack Overflow answer.
template<typename T>
struct function_traits;

template<typename R, typename ...Args>
struct function_traits<std::function<R(Args...)>>
{
	static const size_t nargs = sizeof...(Args);

	template <size_t i>
	struct arg
	{
		typedef typename std::tuple_element<i, std::tuple<Args...>>::type type;
	};
};

#define GENERATE_COMPONENT_GETTERS(ComponentType) \
	ComponentType & GetComponent_ ## ComponentType(ObjectID id);

#define GENERATE_COMPONENT_REMOVERS(ComponentType) \
	bool RemoveComponent_ ## ComponentType (ObjectID id);

#define GENERATE_COMPONENT_CREATORS(ComponentType)						\
	ComponentType & Create_ ## ComponentType (ObjectID id COMPONENT_CONSTRUCTOR_PARAMETERS_ ## ComponentType);

#define GENERATE_COMPONENT_HOLDERS(ComponentType) \
	Leviathan::ComponentHolder< ComponentType > Component ## ComponentType ;

#define GENERATE_SYSTEMS(SystemType) \
	SystemType _ ## SystemType ;

namespace thrive{

class CellStageWorld : public Leviathan::StandardWorld {
public:
	CellStageWorld();
	void _ResetComponents() override;
	void _ResetSystems() override;

	// Component methods.
	#define C_(SystemType) GENERATE_COMPONENT_GETTERS(SystemType)
	COMPONENT_LIST
	#undef C_

	#define C_(SystemType) GENERATE_COMPONENT_REMOVERS(SystemType)
	COMPONENT_LIST
	#undef C_

	#define C_(SystemType) GENERATE_COMPONENT_CREATORS(SystemType)
	COMPONENT_LIST
	#undef C_

	/*
	ProcessorComponent& Create_ProcessorComponent(ObjectID id);
	CompoundBagComponent& Create_CompoundBagComponent(ObjectID id);
	SpeciesComponent& Create_SpeciesComponent(ObjectID id, const std::string &name);
	MembraneComponent& Create_MembraneComponent(ObjectID id);
	CompoundCloudComponent& Create_CompoundCloudComponent(ObjectID id, CompoundId compoundid, float red, float green, float blue);
	AgentCloudComponent& Create_AgentCloudComponent(ObjectID id, CompoundId compoundid, float red, float green, float blue);
	SpawnedComponent& Create_SpawnedComponent(ObjectID id, double newspawnradius);
	CompoundAbsorberComponent& Create_CompoundAbsorberComponent(ObjectID id);
	*/

	void DestroyAllIn(ObjectID id) override;
	std::tuple<void*, bool> GetComponent(ObjectID id, Leviathan::COMPONENT_TYPE type) override;
	//! Helper for getting component of type. This is much slower than
	//! direct lookups with the actual implementation class' GetComponent_Position etc.
	//! methods
	//! \exception NotFound if entity has no component of the wanted type
	//!
	//! This is copied here as a method with the same name would overwrite this otherwise

	template<class TComponent>
	TComponent& GetComponent(ObjectID id){

		std::tuple<void*, bool> component = GetComponent(id, TComponent::TYPE);

		if(!std::get<1>(component))
			throw Leviathan::InvalidArgument("Unrecognized component type as template parameter");

		void* ptr = std::get<0>(component);

		if(!ptr)
			throw Leviathan::NotFound("Component for entity with id was not found");
    
		return *static_cast<TComponent*>(ptr);
	}

	template<class TComponent>
	Leviathan::StateHolder<typename TComponent::StateT>& GetStatesFor() {
		std::tuple<void*, bool> stateHolder = GetStatesFor(TComponent::TYPE);

		if(!std::get<1>(stateHolder))
			throw InvalidArgument("Unrecognized component type as template parameter for "
				"state holder");

		void* ptr = std::get<0>(stateHolder);
    
		return *static_cast<Leviathan::StateHolder<typename TComponent::StateT>*>(ptr);
	}

	std::tuple<void*, bool> GetStatesFor(Leviathan::COMPONENT_TYPE type) override;
	void RunFrameRenderSystems(int tick, int timeintick) override;
	protected:
	void _RunTickSystems() override;
	void HandleAdded() override;
	void ClearAdded() override;
	void _ReleaseAllComponents() override;
	void _DoSystemsInit() override;
	void _DoSystemsRelease() override;

	protected:
	// Components.
	#define C_(ComponentType) GENERATE_COMPONENT_HOLDERS(ComponentType)
	COMPONENT_LIST
	#undef C_

	// Systems.
	#define S_(SystemType) GENERATE_SYSTEMS(SystemType)
	SYSTEM_LIST
	#undef S_
};

}

/*
namespace thrive{

class CellStageWorld : public Leviathan::StandardWorld {
public:
	CellStageWorld();
	void _ResetComponents() override;
	void _ResetSystems() override;
// Component types (8) //
//! \brief Returns a reference to a component of wanted type
//! \exception NotFound when the specified entity doesn't have a component of
//! the wanted type
ProcessorComponent& GetComponent_ProcessorComponent(ObjectID id);
//! \brief Destroys a component belonging to an entity
//! \return True when destroyed, false if the entity didn't have a component 
//! of this type
bool RemoveComponent_ProcessorComponent(ObjectID id);
//! \brief Creates a new component for entity
//! \exception Exception if the component failed to init or it already exists
ProcessorComponent& Create_ProcessorComponent(ObjectID id);

CompoundBagComponent& GetComponent_CompoundBagComponent(ObjectID id);
bool RemoveComponent_CompoundBagComponent(ObjectID id);
CompoundBagComponent& Create_CompoundBagComponent(ObjectID id);

SpeciesComponent& GetComponent_SpeciesComponent(ObjectID id);
bool RemoveComponent_SpeciesComponent(ObjectID id);
SpeciesComponent& Create_SpeciesComponent(ObjectID id, const std::string &name);

MembraneComponent& GetComponent_MembraneComponent(ObjectID id);
bool RemoveComponent_MembraneComponent(ObjectID id);
MembraneComponent& Create_MembraneComponent(ObjectID id);

CompoundCloudComponent& GetComponent_CompoundCloudComponent(ObjectID id);
bool RemoveComponent_CompoundCloudComponent(ObjectID id);
CompoundCloudComponent& Create_CompoundCloudComponent(ObjectID id, CompoundId compoundid, float red, float green, float blue);

AgentCloudComponent& GetComponent_AgentCloudComponent(ObjectID id);
bool RemoveComponent_AgentCloudComponent(ObjectID id);
AgentCloudComponent& Create_AgentCloudComponent(ObjectID id, CompoundId compoundid, float red, float green, float blue);

SpawnedComponent& GetComponent_SpawnedComponent(ObjectID id);
bool RemoveComponent_SpawnedComponent(ObjectID id);
SpawnedComponent& Create_SpawnedComponent(ObjectID id, double newspawnradius);

CompoundAbsorberComponent& GetComponent_CompoundAbsorberComponent(ObjectID id);
bool RemoveComponent_CompoundAbsorberComponent(ObjectID id);
CompoundAbsorberComponent& Create_CompoundAbsorberComponent(ObjectID id);

void DestroyAllIn(ObjectID id) override;
std::tuple<void*, bool> GetComponent(ObjectID id, Leviathan::COMPONENT_TYPE type) override;
//! Helper for getting component of type. This is much slower than
//! direct lookups with the actual implementation class' GetComponent_Position etc.
//! methods
//! \exception NotFound if entity has no component of the wanted type
//!
//! This is copied here as a method with the same name would overwrite this otherwise
template<class TComponent>
TComponent& GetComponent(ObjectID id){

    std::tuple<void*, bool> component = GetComponent(id, TComponent::TYPE);

    if(!std::get<1>(component))
        throw Leviathan::InvalidArgument("Unrecognized component type as template parameter");

    void* ptr = std::get<0>(component);

    if(!ptr)
        throw Leviathan::NotFound("Component for entity with id was not found");
    
    return *static_cast<TComponent*>(ptr);
}

template<class TComponent>
Leviathan::StateHolder<typename TComponent::StateT>& GetStatesFor(){

    std::tuple<void*, bool> stateHolder = GetStatesFor(TComponent::TYPE);

    if(!std::get<1>(stateHolder))
        throw InvalidArgument("Unrecognized component type as template parameter for "
            "state holder");

    void* ptr = std::get<0>(stateHolder);
    
    return *static_cast<Leviathan::StateHolder<typename TComponent::StateT>*>(ptr);
}
std::tuple<void*, bool> GetStatesFor(Leviathan::COMPONENT_TYPE type) override;
void RunFrameRenderSystems(int tick, int timeintick) override;
protected:
void _RunTickSystems() override;
void HandleAdded() override;
void ClearAdded() override;
void _ReleaseAllComponents() override;
void _DoSystemsInit() override;
void _DoSystemsRelease() override;

protected:
Leviathan::ComponentHolder<ProcessorComponent> ComponentProcessorComponent;
Leviathan::ComponentHolder<CompoundBagComponent> ComponentCompoundBagComponent;
Leviathan::ComponentHolder<SpeciesComponent> ComponentSpeciesComponent;
Leviathan::ComponentHolder<MembraneComponent> ComponentMembraneComponent;
Leviathan::ComponentHolder<CompoundCloudComponent> ComponentCompoundCloudComponent;
Leviathan::ComponentHolder<AgentCloudComponent> ComponentAgentCloudComponent;
Leviathan::ComponentHolder<SpawnedComponent> ComponentSpawnedComponent;
Leviathan::ComponentHolder<CompoundAbsorberComponent> ComponentCompoundAbsorberComponent;
MembraneSystem _MembraneSystem;
SpawnSystem _SpawnSystem;
AgentCloudSystem _AgentCloudSystem;
CompoundAbsorberSystem _CompoundAbsorberSystem;
MicrobeCameraSystem _MicrobeCameraSystem;
ProcessSystem _ProcessSystem;

};

}
*/
