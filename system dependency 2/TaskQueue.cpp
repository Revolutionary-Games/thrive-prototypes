#include "TaskQueue.h"

void Mailbox::push(unsigned int taskIndex)
{
	std::lock_guard<std::mutex> lg(lock);
	queuedTasks.push_back(taskIndex);
	cv.notify_one();
}

unsigned int Mailbox::pop()
{
	std::unique_lock<std::mutex> ul(lock);
	cv.wait(ul, [&]() { return !queuedTasks.empty(); });
	const unsigned int taskIndex = queuedTasks.back();
	queuedTasks.pop_back();
	return taskIndex;
}
