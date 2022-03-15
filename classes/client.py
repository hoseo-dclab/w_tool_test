import socket as sock
import numpy as np
import sys, getopt
import time
import cv2

class ClientSocket:

    def __init__(self, img_file, receive_path, address):
        if address.count(':') == 1:
            ip, port = address.split(':')
        else:
            ip = address
            port = 10000

        self.SERVER_IP = ip
        self.SERVER_PORT = int(port)
        self.img_file = img_file
        self.receive_path = receive_path
        self.connect_count = 0
        self.connect_server()

    def connect_server(self):
        try:
            self.socket = sock.socket()
            self.socket.connect((self.SERVER_IP, self.SERVER_PORT))
            print(u'Client connected Server [ ' + self.SERVER_IP + ':' + str(self.SERVER_PORT) + ' ]')
            self.connect_count = 0
            self.client_work()

        except Exception as e:
            print(e)
            self.connect_count += 1
            if self.connect_count == 5:
                print(u'Connected Fail %d times' % self.connect_count)
                sys.exit()
            print(u'%d times fail'% self.connect_count)
            time.sleep(3)
            self.connect_server()

    def client_work(self):
        self.send_images()
        self.receive_images()

    def send_images(self):
        cnt = 0
        try:
            # while os.path.exists(self.img_file):
            encode_image = cv2.imread(self.img_file)
            # print(encode_image.shape)
            data = np.array(encode_image).tobytes()
            length = str(len(data))

            self.socket.sendall(length.encode('utf-8').ljust(64))
            self.socket.sendall(str(encode_image.shape).encode('utf-8').ljust(128))
            self.socket.send(data)
            print(u'send image %d' % cnt)
            cnt+=1
            time.sleep(0.5)

        except Exception as e:
            print(e)
            self.socket.close()
            time.sleep(1)
            self.connect_server()
            self.send_images()

    def receive_images(self):
        try:
            # while True:
            length = self.recvall(self.socket, 64).decode('utf-8')
            print(length)
            shape = self.recvall(self.socket, 128).decode('utf-8')
            print(shape)
            image_list = shape.replace('(', '').replace(')', '').split(',')
            string_data = self.recvall(self.socket, int(length))
            data = np.frombuffer(string_data, np.uint8)
            data = data.reshape(int(image_list[0]), int(image_list[1]), int(image_list[2]))
            cv2.imwrite(self.receive_path + self.img_file[1:], data)

        except Exception as e:
            print(e)
            self.socket.close()
            time.sleep(1)
            self.connect_server()

    def recvall(self, socket, count):
        buf = b''
        while count:
            new_buf = socket.recv(count)
            if not new_buf: return None
            buf += new_buf
            count -= len(new_buf)

        return buf

# def main(address, path, receive_path):
#     address_data = address[0].split(':')
#     print(u'Server IP : ' + address_data[0] + 'Port : ' + address_data[1])
#     client = ClientSocket(address_data[0], int(address_data[1]), path[0], receive_path[0])
#
# def get_arguments():
#     parser = argparse.ArgumentParser()
#     parser.add_argument(nargs='+', help='Address : 127.0.0.1:8080', dest='address')
#     parser.add_argument(nargs='+', help='File Path: ./test_image.png', dest='file_path')
#     parser.add_argument(nargs='+', help='File Path: ./test_image.png', dest='server_receive_path')
#
#     server_addr = parser.parse_args().address
#     file_path = parser.parse_args().file_path
#     server_receive_path = parser.parse_args().server_receive_path
#     return server_addr, file_path, server_receive_path
#
# if __name__ == '__main__':
#     server_addr, file_path, server_receive_path = get_arguments()
#     main(server_addr, file_path, server_receive_path)