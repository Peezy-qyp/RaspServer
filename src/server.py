# -*- coding: utf-8 -*
'''
摄像头常开
'''
from socket import *
import os
import time

import cv2
from cv2 import VideoCapture

import numpy as np
from PIL import Image  
import os
import struct
from threading import Thread

def take_photoes():
    while True:
        ret, frame = cap.read()
        # Our operations on the frame come here
        # Display the resulting frame
        cv2.imshow('frame',frame)
        c = cv2.waitKey(1)
        if c == ord('q'):
            break
        if c == ord('s'):
            path = os.path.join('foo.jpg')
            cv2.imwrite(path,frame)
        return frame

def take_viedo():
    global TakePicture,ImgData
    cap = VideoCapture(0)
    cap.set(3,800)
    cap.set(4,600)
    try:
        while (cap.isOpened()):
            ret_flag, ImgData = cap.read()
            cv2.imshow("Capture_Test", ImgData)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'):
                break
            if TakePicture == True:
                path = os.path.join('test.jpg')
                # cv2.imwrite(path,ImgData)
                print("已拍摄图片")
                TakePicture = False
    except Exception as e:
        cap.release()
        print("摄像头拍摄异常,已推出,错误原因：",e)

def pack_data(_arr):
    # return binary stream
    w = _arr.shape[0]
    h = _arr.shape[1]
    return struct.pack('I',w)+struct.pack('I',h)+_arr.tobytes() # I;4bytes,arr被拉平转为二进制流

def network():
    # 服务器配置
    global TakePicture,ImgData
    myhost = ''
    myport = 8080
    sockobj = socket(AF_INET, SOCK_STREAM) # TCP连接
    sockobj.bind((myhost,myport))
    sockobj.listen(2)
    print ('服务器开始运行...')
    while True: #保持等待连接
        print('等待连接...')
        connection, address = sockobj.accept()
        print ('连接到计算机: ',address)
        while True: # 保持传送数据
            try:
                cmd = connection.recv(2) # 会阻塞程序
                print("接收到: ", cmd)
                if cmd == b'ok':
                    TakePicture = True
                    img = ImgData
                    # img = cv2.imread("test0.png")
                    print(img.shape)
                    packed_data = pack_data(img)
                    data_bytes = len(packed_data)
                    connection.send(data_bytes.to_bytes(4, 'big'))  # 发送即将发送的内容的字节数
                    connection.send(packed_data)  # 发送字节
                    print("发送字节数：", data_bytes)

                if cmd == b'':  #连接断开
                    connection.close()
                    break
            except Exception as e:
                connection.close()
                print("网络接收出现异常,已关闭,异常原因: ", e)

if __name__ == '__main__':
    TakePicture = False # 拍照标志　全局变量　
    ImgData = '' # 拍照数据　全局变量
    photoTask = Thread(target=take_viedo) # 拍摄任务
    networkTask = Thread(target=network) # 网络数据接收任务

    photoTask.start()
    networkTask.start()


