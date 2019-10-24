# -*- coding: utf-8 -*-
"""
    @Author  : LiuZhian
    @Time    : 2019/10/23 0023 下午 8:45
    @Comment : 
"""

# 模拟OS进程调度

from queue import Queue
from task import Task
from systemcall import SystemCall
from select import select


class Scheduler(object):
	def __init__(self):
		# 就绪队列
		self.ready = Queue()
		# 等待其他task退出的等待队列(可能多个任务同时等待一个task，key唯一，value为list)
		self.exit_waiting = {}

		# mapping file descriptor to task
		self.read_waiting = {}  # 等待写队列
		self.write_waiting = {}  # 等待读队列
		# A dictionary that keeps track of all active tasks
		self.task_map = {}

	# 从fd等待数据可读的task
	def wait_for_read(self, task, fd):
		self.read_waiting[fd] = task

	# 从fd等待数据可写的task
	def wait_for_write(self, task, fd):
		self.write_waiting[fd] = task

	def io_poll(self, timeout):
		# I/O Polling. Use select() to determine which file descriptors can be used
		if self.read_waiting or self.write_waiting:
			r, w, e = select(self.read_waiting,
							 self.write_waiting,
							 [], timeout)
			for fd in r:  # 如果有可读数据进来，就把该task重新放回就绪队列，等待调度
				self.schedule(self.read_waiting.pop(fd))
			for fd in w:
				self.schedule(self.write_waiting.pop(fd))

	# 新建一个任务
	def new(self, target):
		new_task = Task(target)
		self.task_map[new_task.tid] = new_task
		self.schedule(new_task)  # 新建好后执行调度
		return new_task.tid

	def schedule(self, task):
		self.ready.put(task)  # 放进就绪队列

	def exit(self, task):
		print("Task %d terminated!" % task.tid)
		del self.task_map[task.tid]  # 模拟释放进程
		# 通知正在等待该即将退出的其他任务，将它们放到就绪队列中去
		for waiting_task in self.exit_waiting.pop(task.tid, []):
			self.schedule(waiting_task)

	def wait_for_exit(self, task, wait_tid):
		"""
		将一个等待wait_tid任务完成的task放进等待队列字典中
		:param task: 正在等待的task
		:param wait_tid: 等待完成的task的tid
		:return: 成功-True，失败 False
		"""
		if wait_tid in self.task_map.keys():
			self.exit_waiting.setdefault(wait_tid, []).append(task)
			return True
		else:  # 等待的是一个根本不存在的task
			return False

	def io_task(self):
		while True:
			# 如果就绪队列为空,就阻塞地轮询多路I/O。
			# 看下是否有准备就绪的I/O，把与之对应的task激活。
			if self.ready.empty():
				# timeout为None时，阻塞地轮询
				self.io_poll(timeout=None)
			else:
				# timeout为None时，非阻塞地轮询一下
				self.io_poll(0)
			yield  # make this func coroutine

	def main_loop(self):
		self.new(self.io_task())  # 新建一个轮询多路I/O的task
		while self.task_map:
			t = self.ready.get()  # 从就绪队列中取出一个
			try:
				# To request the service of the scheduler, tasks
				# will use the yield statement with a value
				result = t.run()  # 再模拟进行一次时间片执行
				if isinstance(result, SystemCall):
					# 下面的这些属性是为了维护环境信息
					# （即包含current task和scheduler的context信息）
					result.task = t
					result.sched = self
					result.handle()
					continue

			except StopIteration:  # 进程执行完毕
				self.exit(t)
				continue
			self.schedule(t)  # 放到就绪队列尾部等待调度
