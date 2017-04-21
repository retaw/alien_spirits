#!/usr/bin/python2.7
# -*- coding: utf-8 -*-  
#coding=utf-8

import subprocess
import socket
import shlex
import time
import sys

def check_tcp_host(ip, port):
    try:
        sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sckt.settimeout(15);
        sckt.connect((ip, port))
    except socket.error as err_msg:
        print err_msg
        return False
    except Exception as e:
        print e
        return False
    return True


def setup_ssh_tunnel(local_port, remote_ip, remote_port):
    try:
        cmd_line_tmp = "ssh -CNR {}:127.0.0.1:{} water@{}"
        cmd_line = cmd_line_tmp.format(remote_port, local_port, remote_ip)
        args = shlex.split(cmd_line)
        print "args:"
        print args
        proc = subprocess.Popen(args)
        print "ssh process id is: {}".format(proc.pid)
    except Exception as e:
        print e
        return None;
    return proc;



def keep_ssh_tunnel(local_port, remote_ip, remote_port):
    proc = setup_ssh_tunnel(local_port, remote_ip, remote_port)
    time.sleep(25)
    while True:
        try:
            #远程端口是否正常打开，如果打开，即认为隧道建立成功, 60s刷新频率
            if check_tcp_host(remote_ip, remote_port):
                time.sleep(60)
                continue;

            #如果进程还在运行，则杀掉
            if proc != None:
                proc.kill()
                print "old process {} is killed".format(proc.pid)

            proc = setup_ssh_tunnel(local_port, remote_ip, remote_port)
            if proc == None:
                print "start ssh process failed!"
            time.sleep(25)

        except:
            print "keep_ssh_tunnel executing error"


def main():
    local_port  = 22
    remote_ip   = "10.173.32.36"
    remote_port = 3022

    if len(sys.argv) == 4:
        local_port  = int(sys.argv[1])
        remote_ip   = sys.argv[2]
        remote_port = int(sys.argv[3])

    keep_ssh_tunnel(local_port, remote_ip, remote_port)
#    print setup_ssh_tunnel(local_port, remote_ip, remote_port)
#    print check_tcp_host(remote_ip, remote_port)

main()
