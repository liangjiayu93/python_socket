#!/usr/bin/env python
# -*- coding:utf-8 -*-

import docker
import socket
import os
import fcntl
import struct
import sys
import threading

num=True
mutex = threading.Lock()

def send_mess(conn,username):
	global num
	print "send:",num
	while (num):
		mess = raw_input()
		if mess == "exit":
			sendmess = username+':'+mess
			print sendmess
			conn.sendall(sendmess)
			print "client exit"
			num = False
		else:
			sendmess = username+':'+mess
			print sendmess
			send_size = conn.sendall(sendmess)
			print "send mess is :%s"%username,mess
			#print send_size
			if send_size:
				print "send mess err"
			else:
				print "send mess succ"
			

def recv_mess(conn,username):
	global num
	print "recv:",num
	while (num):
		data = conn.recv(1024)
		mess = data.split(':')
		if mess[0] == username:
			print "server server:",mess[1]
		else:
			print "server send message err"



def main():
	print "please input your name:"
	username = raw_input()
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect(("192.168.202.132",20000))
	s.sendall("login:%s"%username)
	data = s.recv(1024)
	print data
	mes = data.split(':')
	print "mes[0]=",mes[0]
	print "mes[1]=",mes[1]
	if mes[1] == username:
		print "%s user has already logged in"%mes[1]
		t = threading.Thread(target=recv_mess,args=(s,username))
		t.start()
		send_mess(s,username)
	else:
		print "%s user not connect"%username


if __name__ == "__main__":
    main()