# -*- coding: utf-8 -*-
"""
    @Author  : LiuZhian
    @Time    : 2019/10/24 0024 上午 11:14
    @Comment : 
"""
from socket import *
from systemcall import NewTask, DestroyConn, ReadWait, WriteWait
from scheduler import Scheduler


def handle_client(client, addr):
	"""
	处理客户端请求,简单地将数据echo回客户端
	:param client:
	:param addr:
	:return:
	"""
	print("Connection from", addr)
	while True:
		yield ReadWait(client)
		data = client.recv(65536)
		if data == "q".encode():
			break
		# echo 回显
		yield WriteWait(client)
		client.send(data)

	client.close()
	print("Client closed!")
	# yield 				# make this function a generator/coroutine
	yield DestroyConn()     # My modification (Kill the )




########################################################
#													   #
# 													   #
########################################################

def server(port):
	print("Server starting")
	sock = socket(family=AF_INET, type=SOCK_STREAM)  # TCP连接
	sock.bind(("0.0.0.0", port))
	sock.listen(5)  # 最多监听5个
	while True:
		yield ReadWait(sock)
		client, addr = sock.accept()
		tid = yield NewTask(handle_client(client, addr))


def alive():
	while True:
		print("I'm alive!")
		yield


s = Scheduler()
# s.new(alive())
s.new(server(8877))
s.main_loop()
