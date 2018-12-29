#include "TaskDependencyGraph.h"

void TaskDependencyGraph::init(std::vector<std::vector<unsigned int>> taskInformation)
{
	nodes = std::vector<Node>(taskInformation.size(), Node());

	for(unsigned int i = 0; i < taskInformation.size(); i++)
	{
		for (unsigned int preceedingNode : taskInformation[i])
		{
			nodes[i].numberOfprecedingTasks++;
			nodes[preceedingNode].dependantTasksIndex.push_back(i);
		}
	}
}

std::vector<unsigned int> TaskDependencyGraph::finishTask(unsigned int finishedTaskIndex)
{
	std::vector<unsigned int> result;
	std::lock_guard<std::mutex> lg(lock);

	for(unsigned int dependantTaskIndex : nodes[finishedTaskIndex].dependantTasksIndex)
	{
		nodes[dependantTaskIndex].numberOfprecedingTasksCompleted++;
		if (nodes[dependantTaskIndex].numberOfprecedingTasksCompleted == nodes[dependantTaskIndex].numberOfprecedingTasks)
			result.push_back(dependantTaskIndex);
	}

	return result;
}

void TaskDependencyGraph::reset()
{
	std::lock_guard<std::mutex> lg(lock);
	for (auto& node : nodes) node.numberOfprecedingTasksCompleted = 0;
}
