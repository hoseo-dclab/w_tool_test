import glob
import os
from datetime import datetime
from classes import client

class find_img:

    def __init__(self, filepath, address):
        self.filepath = filepath
        self.address = address
        self.now = datetime.now().strftime("%Y_%m_%d %H.%M.%S")
        self.receive_path = address + '/' + self.now

        self.create_folder(address)
        self.create_folder(self.receive_path)

        self.send_img(self.filepath)

    def create_folder(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def send_img(self, filepath):
        for filename in glob.glob(filepath + "/*"):

            if os.path.isdir(filename):
                found_directory = self.receive_path + filename[1:]
                self.create_folder(found_directory)
                self.send_img(filename)

            else:
                extra = filename.split('.')[-1]
                if extra == "jpg" or extra == "jpeg" or extra == 'png':
                    client.ClientSocket(filename, self.receive_path, self.address)


