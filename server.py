import os
import socket
import logging
from threading import Thread
import re

TCP_IP = ''
TCP_PORT = 9001

# source https://stackoverflow.com/a/59718871


class ClientThread(Thread):
    def __init__(self, ip, port, sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        logging.info(f'New thread started for {ip}:{port}')

    def run(self):
        file_len = int(self.sock.recv(3).decode())
        name_of_file = self.sock.recv(file_len).decode()
        logging.info(f'Get file {name_of_file}')

        list_of_files = os.listdir('.')
        number_of_iterations = list_of_files.count(name_of_file)
        if number_of_iterations > 0:
            name, extension = re.split(r'\.', name_of_file)
            name_of_file = name + '_copy' + \
                str(number_of_iterations) + '.' + extension
            logging.info(f'File was renamed to {name_of_file}')

        with open(name_of_file, 'wb') as sending_file:
            while True:
                fragment = self.sock.recv(512)
                if not fragment:
                    sending_file.close()

                    break
                sending_file.write(fragment)
        logging.info(f'File sended')


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((TCP_IP, TCP_PORT))
    threads = []

    # add logs
    logging.getLogger('requests').setLevel(logging.INFO)
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    while True:
        s.listen()
        logging.info(f'Wait')
        (conn, (ip, port)) = s.accept()

        newthread = ClientThread(ip, port, conn)
        newthread.start()
        threads.append(newthread)

    for t in threads:
        t.join()
