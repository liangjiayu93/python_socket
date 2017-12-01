#!/usr/bin/env python
# -*- coding:utf-8 -*-

#import docker
import socket
import os
import fcntl
import struct
import sys
import threading

class User:
	def __init__(self,sock,username="none"):
		self.sock = sock
		self.username = username

userlist=[]
num = True
senduser = True
recvuser = True

#获取本机IP
def get_ip_address(net_card):
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    host_ip = socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s',net_card[:15]))[20:24])
    s.close()
    return host_ip

def send_mess():
	global senduser
	while senduser:
		print "send mess run"
		print "please input you send user:"
		name = raw_input()
		for i in userlist:
			if i.username == name:
				print "name is find"
				data = raw_input()
				mess = i.username+':'+data
				print "send mess ",mess
				i.sock.sendall(mess)
			else:
				print "name is err,please input again"


def recv_mess(user):
	global recvuser
	while (recvuser):
		print "recv mess run"
		print "recv mess socket ",user.username
		print "recv mess socket ",user.sock
		data = user.sock.recv(1024)
		print "recv mess recv after"
		mess = data.split(':')
		if mess[0] == user.username:
			print "client %s message:"%user.username,mess[1]
		if mess[1] == "exit":
			print "client %s exit:"%user.username
			isuser = False
			user.sock.close()
			for i in userlist:
				if i.username == user.username:
					userlist.remove(i)
					print "client %s remove"%user.username
					print userlist
					#os._exit(0)#网上资料说os._exit用于线程退出，进程退出用sys.exit(0)
					sys.exit(0)#这里我用os._exit会整个程序退出，用sys.exit线程才会退出，这点以后再做深入思考
					#recvuser = False

def find_user():
	user_num = len(userlist)
	print "has %s user"%user_num


def main():
	host_ip = get_ip_address("eth0")
	print host_ip
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	liang = s.bind((host_ip,20000))
	#print liang
	s.listen(5)
	t1 = threading.Thread(target=send_mess)
	t1.setDaemon(True)
	t1.start()
	print "waiting for connection..."
	while True:
		conn,address = s.accept()
		#print conn
		#print address
		data = conn.recv(1024)
		mess = data.split(':')
		user = User(conn)
		user.username = mess[1]
		print "client %s connect succ"%user.username
		#print "user socket %s"%user.sock
		conn.sendall(data)
		userlist.append(user)
		print userlist
		t2 = threading.Thread(target=recv_mess,args=(user,))
		t2.setDaemon(True)
		t2.start()
		usrlis = t2.is_alive()
		#print "usrlis:",usrlis


if __name__ == "__main__":
	main()