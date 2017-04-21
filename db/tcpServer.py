# -*- coding: utf-8 -*-

#
# Author: water - waterlzj@gmail.com
#
# Last modified: 2016-11-12 20:41 +0800
#
# Description:  tcp长连接服务器，用于接收worker进程的数据库操作请求
#               仅服务于少数几个worker进程, 故使用select效率足够了
#


# Msg Structer:
    
import gevent
import gevent.socket
import gevent.select
import json
#import gevent.Queue


class Message:
    S_HEAD = 1
    S_BODY = 2
    S_ERROR = 3
    S_CLOSE = 4

    HEAD_LEN = 8

    def __init__(self):
        self.header = ""
        self.body = ""
        


class DBServer:
    def __init__(self):
        self.listenSckt = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	self.listenSckt.setblocking(False)
	self.listenSckt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR  , 1)
        self.listenSckt.bind(("0.0.0.0", 10001))
	self.listenSckt.listen(10)
 
        
        self.readSckts = [listenSckt]
        self.writeSckts = []

        self.recvMsgQueue = {}
        self.sendMsgQueues = {}

    def start(self):
        while True:
            readable, writable, exceptional = select.select(readSckts, writeSckts, readSckts, 0)
            print "after select"
            for sckt in readable:
                if sckt is listenSckt:
                    connSckt, newRemoteAddr = self.listenSckt.accept()
                    print "new conn from: ", newRemoteAddr
                    connSckt.setblocking(False)
                    self.readSckts.append(connSckt)
                    self.recvMsgQueue[connSckt] = [Message.S_HEAD, Message(), Message.HEAD_LEN, Queue.Queue()]
                else:
                    self.__recv(sckt)
            for sckt in writable:
                self.__send(sckt)



    def __recv(self, sckt):
        state, msg, reserveLen, msgQueue = self.recvMsgQueue[sckt]
        if state == Message.S_ERROR or state == Message.S_CLOSE:
            return

        try:
            newData = sckt.recv(reserveLen)
            recvLen = len(newData)

            #对方已关闭
            if recvLen == 0:
                sckt.close()
                self.recvMsgQueue[connSckt][0] = Message.S_CLOSE
                return

            if state == Message.HEAD:
                msg.header = msg.header + newData
                if(recvLen == reserveLen)
                    self.recvMsgQueue[connSckt][0] = Message.S_BODY
                    self.recvMsgQueue[connSckt][2] = int(msg.header)
            else:
                msg.body = msg.body + newData
                if(recvLen == reserveLen):
                    self.recvMsgQueues[connSckt][0] = Message.S_HEAD
                    self.recvMsgQueues[connSckt][1] = Message()
                    self.recvMsgQueues[connSckt][2] = Message.HEAD_LEN
                    self.recvMsgQueues[connSckt][3].push(msg)
        except socket.error, e:
            errNum = e.args[0]
            if not (errNum == errno.EAGAIN or errNum == errno.EWOULDBLOCK):
                print "recv error: ", e
                self.recvMsgQueues[sckt][0] = Message.S_ERROR
        return
        

    def __send(self, sckt):
        sendLen = sckt.recv


