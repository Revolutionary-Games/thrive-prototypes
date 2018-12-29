#pragma once

#include <vector>
#include <mutex>

class TaskDependencyGraph
{
public:
	// This receives a vector of vectors, where the n-th vector has all the tasks that must be completed before
	// the n-th task can run.
	void init(std::vector<std::vector<unsigned int>> taskInformation);

	// Reports the finalization of a task to the graph.
	// Returns a vector with the tasks that were unlocked by it.
	std::vector<unsigned int> finishTask(unsigned int finishedTaskIndex);

	// Sets all the tasks as unfinished.
	void reset();

private:
	struct Node
	{
		unsigned int numberOfprecedingTasks;
		unsigned int numberOfprecedingTasksCompleted = 0;
		std::vector<unsigned int> dependantTasksIndex;
	};

	std::vector<Node> nodes;

	std::mutex lock; //You can probably replace this with atomics if you want to lose your sanity.
};
