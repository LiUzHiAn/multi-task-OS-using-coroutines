# -*- coding: utf-8 -*-
"""
    @Author  : LiuZhian
    @Time    : 2019/10/23 0023 下午 8:40
    @Comment : 
"""


class Task(object):
	taskid = 0

	def __init__(self, target):
		Task.taskid += 1
		self.tid = Task.taskid
		self.target = target
		self.sendVal = None  # send一个空值，主动执行下一次yield语句

	# run() executes the task to the next yield (a trap)
	def run(self):
		return self.target.send(self.sendVal)


def foo():
	print("one")
	item = yield 1
	print(item)
	print("two")
	item = yield 2
	print(item)


if __name__ == '__main__':
	t = Task(foo())
	print(t.run())
	print(t.run())
