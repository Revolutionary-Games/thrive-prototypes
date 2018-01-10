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

#include "C:/Thrive/src/generated/cell_stage_world.h"

#define COMPONENT_HOLDER_RESET(ComponentType) \
	Component ## ComponentType ## .Clear();

#define SYSTEM_RESET(SystemType) \
	_ ## SystemType ## .Clear();

#define COMPONENT_CLEAR_ADDED(ComponentType)			\
	Component ## ComponentType ## .ClearAdded();		\
	Component ## ComponentType ## .ClearRemoved();

#define COMPONENT_DESTROY_ALL_IN(ComponentType)	\
	Component ## ComponentType ## .Destroy(id, true);

#define COMPONENT_GET_REMOVED(ComponentType)	\
	const auto& removed ## ComponentType = Component ## ComponentType ## .GetRemoved();

#define COMPONENT_GET_ADDED(ComponentType)	\
	const auto& added ## ComponentType = Component ## ComponentType ## .GetRemoved();

#define COMPONENT_DEFINE_REMOVER(ComponentType)							\
bool CellStageWorld::RemoveComponent_ ## ComponentType (ObjectID id) {	\
	try {																\
		Component ## ComponentType ## .Destroy(id, true);				\
		/*_OnComponentDestroyed(id, ComponentType ## ::TYPE());*/		\
		return true;													\
	}																	\
	catch (...) {														\
		return false;													\
	}																	\
}

#define COMPONENT_DEFINE_GETTER(ComponentType)										\
ComponentType & CellStageWorld::GetComponent_## ComponentType (ObjectID id) {		\
	auto component = Component ## ComponentType ## .Find(id);						\
	if (!component)																	\
		throw Leviathan::NotFound("Component for entity with id was not found");	\
																					\
	return *component;																\
}

#define COMPONENT_DEFINE_CONSTRUCTOR(ComponentType)																			\
ComponentType & CellStageWorld::Create_ ## ComponentType (ObjectID id COMPONENT_CONSTRUCTOR_PARAMETERS_ ## ComponentType)	\
{																															\
	return *Component ## ComponentType ## .ConstructNew(id COMPONENT_CONSTRUCTOR_ARGUMENTS_ ## ComponentType);				\
}

#define COMPONENT_GET_COMPONENT_SWITCH_CASE(ComponentType)					\
case static_cast<uint16_t>( ComponentType ## ::TYPE) :						\
{																			\
	return std::make_tuple(Component ## ComponentType ##.Find(id), true);	\
} // shouldn't this break?

namespace thrive{

CellStageWorld::CellStageWorld(){}
void CellStageWorld::_ResetComponents(){
	// Reset all component holders //
	#define C_(ComponentType) COMPONENT_HOLDER_RESET(ComponentType)
	COMPONENT_LIST
	#undef C_
}

void CellStageWorld::_ResetSystems(){
	// Reset all system nodes //
	#define S_(SystemType) SYSTEM_RESET(SystemType)
	SYSTEM_LIST
	#undef S_
}

// Component types (8) //
#define C_(ComponentType) COMPONENT_DEFINE_GETTER(ComponentType)
COMPONENT_LIST
#undef C_

#define C_(ComponentType) COMPONENT_DEFINE_REMOVER(ComponentType)
COMPONENT_LIST
#undef C_

#define C_(ComponentType) COMPONENT_DEFINE_CONSTRUCTOR(ComponentType)
COMPONENT_LIST
#undef C_

/*
ProcessorComponent& CellStageWorld::Create_ProcessorComponent(ObjectID id)
{
	return *ComponentProcessorComponent.ConstructNew(id);
}

CompoundBagComponent& CellStageWorld::Create_CompoundBagComponent(ObjectID id)
{
	return *ComponentCompoundBagComponent.ConstructNew(id);
}

SpeciesComponent& CellStageWorld::Create_SpeciesComponent(ObjectID id, const std::string &name)
{
	return *ComponentSpeciesComponent.ConstructNew(id, name);
}

MembraneComponent& CellStageWorld::Create_MembraneComponent(ObjectID id)
{
	return *ComponentMembraneComponent.ConstructNew(id);
}

CompoundCloudComponent& CellStageWorld::Create_CompoundCloudComponent(ObjectID id, CompoundId compoundid, float red, float green, float blue)
{
	return *ComponentCompoundCloudComponent.ConstructNew(id, compoundid, red, green, blue);
}

AgentCloudComponent& CellStageWorld::Create_AgentCloudComponent(ObjectID id, CompoundId compoundid, float red, float green, float blue)
{
	return *ComponentAgentCloudComponent.ConstructNew(id, compoundid, red, green, blue);
}

SpawnedComponent& CellStageWorld::Create_SpawnedComponent(ObjectID id, double newspawnradius)
{
	return *ComponentSpawnedComponent.ConstructNew(id, newspawnradius);
}

CompoundAbsorberComponent& CellStageWorld::Create_CompoundAbsorberComponent(ObjectID id)
{
	return *ComponentCompoundAbsorberComponent.ConstructNew(id);
}
*/

void CellStageWorld::DestroyAllIn(ObjectID id) {
	Leviathan::StandardWorld::DestroyAllIn(id);

	#define C_(ComponentType) COMPONENT_DESTROY_ALL_IN(ComponentType)
	COMPONENT_LIST
	#undef C_
}

std::tuple<void*, bool> CellStageWorld::GetComponent(ObjectID id, Leviathan::COMPONENT_TYPE type){
	const auto baseType = Leviathan::StandardWorld::GetComponent(id, type);
	if(std::get<1>(baseType))
		return baseType;

		switch(static_cast<uint16_t>(type)){
			#define C_(ComponentType) COMPONENT_GET_COMPONENT_SWITCH_CASE(ComponentType)
			COMPONENT_LIST
			#undef C_
		default:
			return std::make_tuple(nullptr, false);
		}
}

std::tuple<void*, bool> CellStageWorld::GetStatesFor(Leviathan::COMPONENT_TYPE type){
const auto baseType = Leviathan::StandardWorld::GetStatesFor(type);
if(std::get<1>(baseType))
    return baseType;

switch(static_cast<uint16_t>(type)){
default:
return std::make_tuple(nullptr, false);
}
}
void CellStageWorld::RunFrameRenderSystems(int tick, int timeintick){
Leviathan::StandardWorld::RunFrameRenderSystems(tick, timeintick);



}
void CellStageWorld::_RunTickSystems(){
Leviathan::StandardWorld::_RunTickSystems();
  const auto timeAndTickTuple = GetTickAndTime();
  const auto calculatedTick = std::get<0>(timeAndTickTuple);
  const auto progressInTick = std::get<1>(timeAndTickTuple);
  const auto tick = GetTickNumber();

// Begin of group 5 //
_AgentCloudSystem.Run(*this);
// Begin of group 6 //
_CompoundAbsorberSystem.Run(*this, ComponentCompoundCloudComponent.GetIndex());
// Begin of group 10 //
_ProcessSystem.Run(*this);
// Begin of group 50 //
_SpawnSystem.Run(*this);
// Begin of group 100 //
_MembraneSystem.Run(*this, GetScene());
// Begin of group 1000 //
_MicrobeCameraSystem.Run(*this);
}
void CellStageWorld::HandleAdded(){
Leviathan::StandardWorld::HandleAdded();

#define C_(ComponentType) COMPONENT_GET_ADDED(ComponentType)
COMPONENT_LIST
#undef C_

// Component types of parent type
const auto& addedRenderNode = ComponentRenderNode.GetAdded();
const auto& removedRenderNode = ComponentRenderNode.GetRemoved();
const auto& addedPosition = ComponentPosition.GetAdded();
const auto& removedPosition = ComponentPosition.GetRemoved();


// Added
if(!addedMembraneComponent.empty() || !addedRenderNode.empty()){
    _MembraneSystem.CreateNodes(
        addedMembraneComponent, addedRenderNode,
        ComponentMembraneComponent, ComponentRenderNode);
}
if(!addedPosition.empty() || !addedAgentCloudComponent.empty() || !addedRenderNode.empty()){
    _AgentCloudSystem.CreateNodes(
        addedPosition, addedAgentCloudComponent, addedRenderNode,
        ComponentPosition, ComponentAgentCloudComponent, ComponentRenderNode);
}
if(!addedAgentCloudComponent.empty() || !addedPosition.empty() || !addedMembraneComponent.empty() || !addedCompoundAbsorberComponent.empty()){
    _CompoundAbsorberSystem.CreateNodes(
        addedAgentCloudComponent, addedPosition, addedMembraneComponent, addedCompoundAbsorberComponent,
        ComponentAgentCloudComponent, ComponentPosition, ComponentMembraneComponent, ComponentCompoundAbsorberComponent);
}
if(!addedCompoundBagComponent.empty() || !addedProcessorComponent.empty()){
    _ProcessSystem.CreateNodes(
        addedCompoundBagComponent, addedProcessorComponent,
        ComponentCompoundBagComponent, ComponentProcessorComponent);
}
// Removed
#define C_(ComponentType) COMPONENT_GET_REMOVED(ComponentType)
COMPONENT_LIST
#undef C_

if(!removedMembraneComponent.empty() || !removedRenderNode.empty()){
    _MembraneSystem.DestroyNodes(
        removedMembraneComponent, removedRenderNode);
}
if(!removedPosition.empty() || !removedAgentCloudComponent.empty() || !removedRenderNode.empty()){
    _AgentCloudSystem.DestroyNodes(
        removedPosition, removedAgentCloudComponent, removedRenderNode);
}
if(!removedAgentCloudComponent.empty() || !removedPosition.empty() || !removedMembraneComponent.empty() || !removedCompoundAbsorberComponent.empty()){
    _CompoundAbsorberSystem.DestroyNodes(
        removedAgentCloudComponent, removedPosition, removedMembraneComponent, removedCompoundAbsorberComponent);
}
if(!removedCompoundBagComponent.empty() || !removedProcessorComponent.empty()){
    _ProcessSystem.DestroyNodes(
        removedCompoundBagComponent, removedProcessorComponent);
}
}

void CellStageWorld::ClearAdded(){
	Leviathan::StandardWorld::ClearAdded();

	#define C_(ComponentType) COMPONENT_CLEAR_ADDED(ComponentType)
	COMPONENT_LIST
	#undef C_
}

void CellStageWorld::_ReleaseAllComponents(){
Leviathan::StandardWorld::_ReleaseAllComponents();

ComponentMembraneComponent.ReleaseAllAndClear(GetScene());
}

void CellStageWorld::_DoSystemsInit(){
// Call Init on all systems that need it //
}

void CellStageWorld::_DoSystemsRelease(){
// Call Release on all systems that need it //
}

}
