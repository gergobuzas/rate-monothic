import math


class Task:
	def __init__(self, task_name, capacity_time, period_time, arrive_time) -> None:
		self.name = task_name
		self.capacity = capacity_time
		self.period_time = period_time
		self.first_arrive_time = arrive_time

class DMA:
	def __init__(self):
		self.tasks = list[Task]()

	def add_task(self, task: Task):
		self.tasks.append(task)
	
	def get_dma(self):
		print()
		print("DMA for the added tasks (2.3a)")
		print()
		step = 0
		r = 0
		i = 0
		last_task_idx = len(self.tasks) - 1
		rnew = self.tasks[last_task_idx].capacity
		originalrnew = rnew
		while (r != rnew):
			print("Step " + str(step) + "\tr:" + str(r) + " i:" + str(i) + " rnew:" + str(rnew))

			r = rnew
			i = 0
			for idx in range(len(self.tasks) - 1):
				task_to_compare = self.tasks[idx]
				i += task_to_compare.capacity * math.ceil(r / task_to_compare.period_time)
			rnew = originalrnew + i

			step += 1
		print("Step " + str(step) + "\tr:" + str(r) + " i:" + str(i) + " rnew:" + str(rnew))
	
	def get_max_capacities(self):
		print()
		print("Max capacities for each tasks (2.3b)")
		print()

		# Getting the biggest period
		max_period = 0
		for task in self.tasks:
			if task.period_time > max_period:
				max_period = task.period_time
		
		for i in range(len(self.tasks)):
			print("Results for task" + str(i+1))
			task_to_find_max = self.tasks[i]
			current_period_val = max_period
			for task in self.tasks:
				if task != self.tasks[i]:
					current_period_val = current_period_val - (max_period / task.period_time * task.capacity)
			current_period_val = current_period_val / (max_period / task_to_find_max.period_time)

			print("\tmax capacity:\t" + str(current_period_val))

			
		

    

if __name__ == "__main__":
	dma = DMA()
	task1 = Task("task1", 4, 16, 0)
	task2 = Task("task2", 6, 32, 0)
	task3 = Task("task3", 8, 64, 0)
	task4 = Task("task4", 30, 128, 0)

	#task1 = Task("task1", 6, 24, 0)
	#task2 = Task("task2", 9, 48, 0)
	#task3 = Task("task3", 12, 96, 0)
	#task4 = Task("task4", 45, 192, 0)

	#task1 = Task("task1", 2, 10, 0)
	#task2 = Task("task2", 2, 50, 0)
	#task3 = Task("task3", 10, 50, 0)
	#task4 = Task("task4", 30, 80, 0)

	dma.add_task(task1)
	dma.add_task(task2)
	dma.add_task(task3)
	dma.add_task(task4)

	dma.get_dma()
	dma.get_max_capacities()