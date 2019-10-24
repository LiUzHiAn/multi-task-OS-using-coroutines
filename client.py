# -*- coding: utf-8 -*-
"""
    @Author  : LiuZhian
    @Time    : 2019/10/24 0024 下午 4:13
    @Comment : 
"""

from socket import *

host = "127.0.0.1"
port = 8877
client_sock = socket(AF_INET, SOCK_STREAM)
client_sock.connect((host, port))

# client_sock.send("Hello,this is client socket".encode())
while True:
	msg = input("请输入要发送到服务端的数据(按q退出)：")
	if msg == "q":
		client_sock.send(msg.encode())
		break
	client_sock.send(msg.encode())
	recv_data = client_sock.recv(65535)
	if not recv_data:
		break
	print(recv_data.decode())
