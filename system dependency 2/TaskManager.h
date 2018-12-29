#pragma once

#include "TaskDependencyGraph.h"
#include "TaskQueue.h"

#include <condition_variable>
#include <mutex>
#include <string>
#include <thread>
#include <vector>

#define FIRST_TASK_IDENTIFIER "__first"
#define LAST_TASK_IDENTIFIER "__last"
#define DUMMY_TASK_IDENTIFIER "__dummy"

#define DUMMY_TASK_INDEX 0
#define FIRST_TASK_INDEX 1
#define LAST_TASK_INDEX 2

const unsigned int NUMBER_OF_THREADS = std::thread::hardware_concurrency();

struct TaskInformation
{
	std::function<void()> task;
	std::string name;
	std::vector<std::string> precedingTasks;
};

class TaskManager
{
public:
	// Initializes threads and internal tasks.
	TaskManager();

	// Must join all the threads.
	~TaskManager();

	// Adds a task to the system, must be called before generateDependencyGraph().
	void addTask(const TaskInformation& taskInformation);

	// Generates the graph and allows for run() to be called.
	void generateDependencyGraph();

	// Runs all the tasks in the correct order. Must have run generateDependencyGraph() before.
	void run();

private:
	Mailbox taskQueue;
	TaskDependencyGraph taskDependencyGraph;

	bool beingDestroyed = false;
	std::vector<TaskInformation> tasks;
	std::vector<std::thread> threadPool;

	bool isDone;
	std::mutex lock;
	std::condition_variable cv;
};
