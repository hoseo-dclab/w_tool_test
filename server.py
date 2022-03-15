import os
import socket as sock
import threading
import numpy as np
import cv2
from classes import config


class ServerSocket:

    def __init__(self):
        self.data = None
        self.socket = None
        self.IP = config.ip
        self.PORT = config.port
        self.save_dir = config.save_directory
        self.file_path = ''
        self.system_call = config.sys_call
        self.system_call_result = ''
        self.socket_open()
        self.receive_thread = threading.Thread(target=self.server_work())
        self.receive_thread.start()

    def socket_close(self):
        self.socket.close()
        print(u'server closed [ IP: ' + self.IP + ', PORT: ' + str(self.PORT) + ' ]')

    def socket_open(self):
        self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
        self.socket.bind((self.IP, self.PORT))
        self.socket.listen(100)
        print(u'server opened [ IP: ' + self.IP + ', PORT: ' +str(self.PORT) + ' ]')


    def server_work(self):
        while True:
            self.conn, self.addr = self.socket.accept()
            print(u'server connected [ IP: ' + self.IP + ', PORT: ' + str(self.PORT) + ' ]')
            self.receive_images()
            self.system_work()
            self.send_system_result()
            self.send_images()
            self.save_data()
            self.conn.close()

    def system_work(self):
        print(self.system_call)
        stream = os.popen(self.system_call)
        self.system_call_result = stream.read()

    def send_system_result(self):
        print(self.system_call_result)

    def save_data(self):
        self.file_path = self.save_dir + '/' + self.system_call_result + '.png'
        print(self.file_path)
        cv2.imwrite(self.file_path, self.data)
        self.data = None

    def send_images(self):
        encode_image = self.data
        print(encode_image.shape)
        data = np.array(encode_image).tobytes()
        length = str(len(data))
        self.conn.sendall(length.encode('utf-8').ljust(64))
        self.conn.sendall(str(encode_image.shape).encode('utf-8').ljust(128))
        self.conn.send(data)
        print('send_images_end')

    def receive_images(self):
        try:
            length = self.recvall(self.conn, 64).decode('utf-8')
            print(length)
            shape = self.recvall(self.conn, 128).decode('utf-8')
            print(shape)
            image_list = shape.replace('(', '').replace(')', '').split(',')
            string_data = self.recvall(self.conn, int(length))
            data = np.frombuffer(string_data, np.uint8)
            self.data = data.reshape(int(image_list[0]), int(image_list[1]), int(image_list[2]))

        except Exception as e:
            print(e)
            self.socket_close()
            self.socket_open()
            self.receive_thread = threading.Thread(target=self.server_work())
            self.receive_thread.start()

    def recvall(self, socket, count):
        buf = b''
        while count:
            new_buf = socket.recv(count)
            if not new_buf: return None
            buf += new_buf
            count -= len(new_buf)

        return buf

def main():
    server = ServerSocket()

if __name__ == "__main__":
    main()
