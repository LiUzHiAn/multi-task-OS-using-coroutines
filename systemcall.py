# -*- coding: utf-8 -*-
"""
    @Author  : LiuZhian
    @Time    : 2019/10/23 0023 下午 9:30
    @Comment : 
"""


# syscall 基类
class SystemCall(object):
	def handle(self):
		pass


class GetTid(SystemCall):
	def handle(self):
		self.task.sendVal = self.task.tid
		self.sched.schedule(self.task)


class NewTask(SystemCall):
	def __init__(self, target):
		self.target = target

	def handle(self):
		# 新创建的任务的tid
		tid = self.sched.new(self.target)
		# NewTask()对象本身这个task的sendVal设置为创建出来的task的tid
		self.task.sendVal = tid
		self.sched.schedule(self.task)


class KillTask(SystemCall):
	def __init__(self, tid):
		self.tid = tid

	def handle(self):
		task = self.sched.task_map.get(self.tid, None)
		if task:  # 如果的确存在该task,则kill掉
			task.target.close()  # 吧coroutine shutdown掉
			self.task.sendVal = True  # True 表示kill task成功
		else:
			self.task.sendVal = False
		self.sched.schedule(self.task)


class WaitTask(SystemCall):
	def __init__(self, wait_tid):
		self.wait_tid = wait_tid

	def handle(self):
		result = self.sched.wait_for_exit(task=self.task, wait_tid=self.wait_tid)
		self.task.sendVal = result  # True表示等待成功
		if not result:
			self.sched.shcedule(self.task)  # 把自己加入就绪队列等待轮训


class DestroyConn(SystemCall):
	def handle(self):
		self.sched.exit(self.task)

class ReadWait(SystemCall):
	def __init__(self, f):
		self.f = f

	def handle(self):
		fd = self.f.fileno()  # 得到文件对应OS底层的fd
		self.sched.wait_for_read(self.task, fd)


class WriteWait(SystemCall):
	def __init__(self, f):
		self.f = f

	def handle(self):
		fd = self.f.fileno()  # 得到文件对应OS底层的fd
		self.sched.wait_for_write(self.task, fd)
