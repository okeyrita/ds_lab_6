import os
import sys
import socket
import logging
from tqdm import tqdm

TCP_PORT = 9001


def main(name_of_file, address, port):
    # source https://stackoverflow.com/a/59718871
    # create socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((address, int(port)))
    s.send(str.encode(f'{len(name_of_file):03d}'))
    s.send(str.encode(name_of_file))

    # send file
    logging.info(f'Send file {name_of_file}')
    with open(name_of_file, 'rb') as sending_file:
        # source of tqdm https://www.geeksforgeeks.org/python-how-to-make-a-terminal-progress-bar-using-tqdm/
        progress_of_transferring = tqdm(total=os.path.getsize(name_of_file))

        fragment = sending_file.read(512)
        while fragment:
            s.send(fragment)
            progress_of_transferring.update(512)
            fragment = sending_file.read(512)

        progress_of_transferring.close()
        logging.info(f'File {name_of_file} sended')

    s.close()
    logging.info(f'End of connection')


if __name__ == "__main__":
    # get useful data
    name_of_file = sys.argv[1]
    address = sys.argv[2]
    port = sys.argv[3]

    # add logs
    logging.getLogger('requests').setLevel(logging.INFO)
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    main(name_of_file, address, port)
