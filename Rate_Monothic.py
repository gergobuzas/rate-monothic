import math
import json
from typing import List


class Task:
	def __init__(self, task_name, capacity_time, period_time, arrive_time) -> None:
		self.name = task_name
		self.capacity = capacity_time
		self.period_time = period_time
		self.first_arrive_time = arrive_time


class Period:
	def __init__(self, task: Task, added_to_start_time, resolution):
		self.task = task
		self.period_start_time = task.first_arrive_time + added_to_start_time
		self.period_end_time = self.period_start_time + task.period_time
		self.current_capacity = 0.0
		self.resolution = resolution
		self.finished = False
		self.started = False
		self.run_at = list()
		self.started_at = None
		self.finished_at = None

	def check_done(self) -> bool :
		if self.current_capacity == self.task.capacity:
			self.finished = True
		return self.finished

	def can_be_started(self, current_time):
		if current_time >= self.period_start_time:
			return True
		return False

	def run(self, current_time):
		if self.started == False:
			self.started = True
			self.started_at = current_time
			print(self.task.name + " started at: " + str(current_time) )
		self.current_capacity += self.resolution
		self.current_capacity = round(self.current_capacity, 3)
		self.run_at.append(current_time)
		is_done = self.check_done()
		if is_done:
			self.finished_at = current_time
			print(self.task.name + " finished at: " + str(current_time) + "\t Current capacity: " + str(self.current_capacity))


dead_time=list()
class RateMonothicScheduler:
	def __init__(self, schedule_period, schedule_delay, resolution) -> None:
		# schedule_period --> How frequent we reschedule
		# schedule_delay --> The delay between the rescheduling and switching to the newly scheduled task
		# resolution --> The increments in which our scheduler should increment
		self.reschedule_frequency = schedule_period
		self.schedule_delay = schedule_delay
		self.resolution = resolution
		self.periods = None
		self.periods_to_run_for_delay = None
		self.task_list = None
		self.current_periods = None
		self.lcm = 0.0
   
	def check_lcm(self):
		periods = list()
		for task in self.task_list:
			periods.append(task.period_time)
		self.lcm = math.lcm(*periods)

	def create_periods_for_task(self, task: Task):
		print(self.lcm)
		print(task.period_time)
		amount_of_periods_for_task = math.ceil( (self.lcm - task.first_arrive_time) / task.period_time )
		print(amount_of_periods_for_task)
		for i in range(amount_of_periods_for_task):
			period = Period(task, i * task.period_time, self.resolution)		
			if self.periods == None:
				self.periods: list[Period] = list()
			self.periods.append(period)
	
	def create_periods(self):
		for task in self.task_list:
			self.create_periods_for_task(task)

	def add_task(self, task: Task):
		if self.task_list is None:
			self.task_list: List[Task] = list()
		self.task_list.append(task)

	def insert_into_current_periods(self, period_to_add: Period):
		if len(self.current_periods) == 0:
			self.current_periods.append(period_to_add)	
			return
		
		was_inserted = False
		for i in range(len(self.current_periods)):
			compared_period = self.current_periods[i]
			is_higher_prio = period_to_add.task.period_time < compared_period.task.period_time
			if is_higher_prio:
				self.current_periods.insert(i, period_to_add)
				was_inserted = True
		
		if was_inserted == False:
			self.current_periods.append(period_to_add)
 
	def reschedule(self, current_time) -> bool:
		is_first = self.current_periods is None
		old_current = self._get_old_current_periods() if not is_first else []
		self._update_current_periods(current_time)
		changed_current = self._has_current_period_changed(is_first, old_current)
		return changed_current

	def _get_old_current_periods(self) -> List[Period]:
		return list(self.current_periods)

	def _update_current_periods(self, current_time):
		self.current_periods = []
		for period in self.periods:
			if period.can_be_started(current_time) and not period.check_done():
				self.insert_into_current_periods(period)

	def _has_current_period_changed(self, is_first, old_current) -> bool:
		if is_first:
			return False
		if not old_current or old_current[0].task.name != self.current_periods[0].task.name or len(old_current) != len(self.current_periods):
			self.periods_to_run_for_delay = old_current
			return True
		return False
			
	
	def get_period_to_run(self):
		if self.current_periods == None:
			return None
		# Removing finished periods
		periods_to_remove = list()
		for period in self.current_periods:
			if period.check_done() == True:
				periods_to_remove.append(period)
		for period in periods_to_remove:
			self.current_periods.remove(period)

		for period in self.current_periods:
			if period.check_done() == False:
				return period
		

		return None

	def run_period(self, period_to_run: Period, current_time):
		print("Time: " + str(round(current_time, 3)) + "\tRunning period: " + str(period_to_run.task.name))
		period_to_run.run(current_time)


	def get_period_to_run_delay(self):
		for period in self.periods_to_run_for_delay:
			if period.check_done() == False:
				return period
			else:
				self.periods_to_run_for_delay.remove(period)
		return None

	def run_period_during_delay(self, current_time):
		delay_periods = int( round(self.schedule_delay, 3) / round(self.resolution, 3))
		for i in range(delay_periods):
			period_to_run = self.get_period_to_run_delay()
			if period_to_run == None:
				time = current_time + round(i * self.resolution, 3)
				print("Dead time at: " + str(time) + " ms --- no task to run")
				dead_time.append(time)
			else:
				time = current_time + round(i * self.resolution, 3)
				self.run_period(period_to_run, time)


	def run_scheduling(self):
		self.check_lcm()
		self.create_periods()

		time = 0.0
		while time <= self.lcm:
			time = round(time, 3)
			current_period_changed = False
			modulo = math.fmod(time, self.reschedule_frequency)
			if modulo == 0:
				current_period_changed = self.reschedule(time)

			if (current_period_changed):
				self.run_period_during_delay(time)
				time += self.schedule_delay
			else:
				period_to_run = self.get_period_to_run()
				if period_to_run != None:
					self.run_period(period_to_run, time)
				else:
					print("Dead time at: " + str(time) + " ms --- no task to run")
					dead_time.append(time)
				time += self.resolution
	
	def export_results(self, export_location = "result.json"):
		results = dict()
		# Getting the task names
		task_names = list()
		for period in self.periods:
			if period.task.name not in task_names:
				task_names.append(period.task.name)
		
		# Getting where each task was run at
		for name in task_names:
			list_for_name = list()
			for period in self.periods:
				if period.task.name == name:
					list_for_name.extend(period.run_at)
			results[name] = list_for_name

		# Getting the dead times
		results["deadTime"] = dead_time
		results["sumDeadTime"] = len(dead_time) * self.resolution
		results["resolution"] = self.resolution
		
		print(results)
		# Exporting to file
		with open(export_location, 'w') as file:
			json.dump(results, file)
			


if __name__ == "__main__":
	scheduler = RateMonothicScheduler(4, 0.5, 0.1)

	task1 = Task("task1", 4, 16, 18.1)
	task2 = Task("task2", 6, 32, 2.2)
	task3 = Task("task3", 8, 64, 4.3)
	task4 = Task("task4", 30, 128, 0.4)
	scheduler.add_task(task1)
	scheduler.add_task(task2)
	scheduler.add_task(task3)
	scheduler.add_task(task4)

	scheduler.run_scheduling()
	scheduler.export_results()
