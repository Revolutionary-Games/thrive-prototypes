#include "TaskManager.h"

#include <algorithm>

TaskManager::TaskManager()
{
	for (unsigned int i = 0; i < NUMBER_OF_THREADS; i++) {
		threadPool.emplace_back([&]()
		{
			while(!beingDestroyed)
			{
				const unsigned int nextTaskIndex = taskQueue.pop();
				tasks[nextTaskIndex].task();
				const auto unlockedTasks = taskDependencyGraph.finishTask(nextTaskIndex);
				for (auto index : unlockedTasks) taskQueue.push(index);
			}
		});
	}

	// This task is used to terminate all the threads.
	TaskInformation dummyTask;
	dummyTask.name = DUMMY_TASK_IDENTIFIER;
	dummyTask.task = []() {};
	tasks.push_back(dummyTask);

	// This task is used to signal a new tick.
	TaskInformation firstTask;
	firstTask.name = FIRST_TASK_IDENTIFIER;
	firstTask.task = []() {};
	tasks.push_back(firstTask);

	// This task is used to return control to the world.
	TaskInformation lastTask;
	lastTask.name = LAST_TASK_IDENTIFIER;
	lastTask.task = [&]()
	{
		std::unique_lock<std::mutex> ul(lock);
		isDone = true;
		cv.notify_one();
		taskDependencyGraph.reset();
	};
	tasks.push_back(lastTask);
}

TaskManager::~TaskManager()
{
	beingDestroyed = true;
	for (auto& thr : threadPool) taskQueue.push(DUMMY_TASK_INDEX);
	for (auto& thr : threadPool) thr.join();
}

void TaskManager::addTask(const TaskInformation& taskInformation)
{
	tasks.push_back(taskInformation);
}

void TaskManager::generateDependencyGraph()
{
	// Adding the dependency of the first task to every other task.
	for (unsigned int i = FIRST_TASK_INDEX + 1; i < tasks.size(); i++) tasks[i].precedingTasks.emplace_back(FIRST_TASK_IDENTIFIER);

	// Adding the dependency of every user-created task to the last task.
	for (unsigned int i = LAST_TASK_INDEX + 1; i < tasks.size(); i++) tasks[LAST_TASK_INDEX].precedingTasks.push_back(tasks[i].name);

	std::vector<std::vector<unsigned int>> dependencies(tasks.size(), std::vector<unsigned int>());

	for (unsigned int i = 0; i < tasks.size(); i++)
	{
		for (unsigned int j = 0; j < tasks.size(); j++)
		{
			if(std::find(tasks[i].precedingTasks.begin(), tasks[i].precedingTasks.end(), tasks[j].name) != tasks[i].precedingTasks.end())
			{
				dependencies[i].push_back(j);
			}
		}
	}

	taskDependencyGraph.init(dependencies);
}

void TaskManager::run()
{
	isDone = false;
	std::unique_lock<std::mutex> ul(lock);
	taskQueue.push(FIRST_TASK_INDEX);
	cv.wait(ul, [&]() { return isDone; });
}
