#pragma once

#include <condition_variable>
#include <mutex>
#include <vector>

class Mailbox
{
public:
	// Pushes a task index to the queue in a threadsafe way.
	void push(unsigned int taskIndex);

	// Pops a task index from the queue in a threadsafe way, or waits until
	// one is available if the queue is empty.
	unsigned int pop();

private:
	std::vector<unsigned int> queuedTasks;

	std::condition_variable cv;
	std::mutex lock;
};
