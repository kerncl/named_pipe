import time
import logging
import win32pipe, win32file
import subprocess
import sys


format = '%(asctime)s [%(levelname)s]: %(message)s'
logging.basicConfig(format=format, level=logging.INFO, datefmt='%H:%M:%S')


def pipe_server():
    logging.info('pipe server start ...')
    count = 0
    pipe = win32pipe.CreateNamedPipe(
        r'\\.\pipe\testpipe',   # pipe name \\.\pipe\<pipename>
        win32pipe.PIPE_ACCESS_DUPLEX,   # open mode
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,    # pipe mode
        1,  # max Instance for the pipe
        65536,  # Out buffer size eg: 16bit
        65536,  # In buffer size eg:  16bit
        0,  # default time out
        None)   # Security attribute
    try:
        logging.info('Waiting response from client')
        win32pipe.ConnectNamedPipe(
            pipe,
            None)
        logging.info('Received respond from client ')
        # while count < 10:
        #     # convert to bytes
        #     some_data = str(count).encode()
        #     logging.info(f'Generate data {some_data}')
        #     p = subprocess.Popen([sys.executable, 'print_input.py'],
        #                          stdin=subprocess.PIPE,
        #                          stdout=subprocess.PIPE,
        #                          stderr=subprocess.PIPE)
        #     out, err = p.communicate(input=some_data)
        #     logging.info(f'writing message {out}')
        #     win32file.WriteFile(    # return error code
        #         pipe,   # filehandle
        #         out)  # string
        #     time.sleep(1)
        #     count += 1
        # logging.info('finihsed')
        loop = True
        while loop:
            hr, msg = win32file.ReadFile(
                pipe,
                64*1024
            )
            if not hr:
                logging.info(f'Received input message: {msg}')
                p = subprocess.Popen([sys.executable, 'print_input.py'],
                                     stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
                out, err = p.communicate(input=msg)
                logging.info(f'writing message {out}')
                win32file.WriteFile(
                    pipe,
                    out
                )
                logging.info(f'Done sent message')
                time.sleep(1)
                msg = msg.decode()
                if 'stop' in msg:
                    logging.info(f'Stopping')
                    loop = False
    finally:
        win32file.CloseHandle(pipe)


if __name__ == '__main__':
    pipe_server()
