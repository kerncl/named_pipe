import logging
import time
import win32file, win32pipe, pywintypes


format = '%(asctime)s [%(levelname)s]: %(message)s'
logging.basicConfig(format=format, level=logging.INFO, datefmt='%H:%M:%S')


def pipe_client():
    logging.info('pipe client')
    quit = False
    while not quit:
        try:
            handle = win32file.CreateFile(  # Return Pyhandle object
                r'\\.\pipe\testpipe',   # pipe file name
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,   # desired access
                0,  # Share mode 0 (once connected, file cannot be shared)
                None,   # SecurityAttributes
                win32file.OPEN_EXISTING,    # Creation Disposition (action to the file if exists/non-exists)
                0,  # flags and attributes
                None    # Template file
            )
            res = win32pipe.SetNamedPipeHandleState(
                handle,
                win32pipe.PIPE_READMODE_MESSAGE,
                None,
                None
            )
            if not res:
                logging.error(f'SetNamePipeHandleState return code: {res}')
            loop = True
            while loop:
                logging.info('Please key in some input:')
                _ = input()
                _ = str(_).encode()
                win32file.WriteFile(
                    handle,
                    _
                )
                time.sleep(2)
                hr, msg = win32file.ReadFile(  # Return 0 / ERROR_IO_PENDING
                    handle, # fileHandle: obtain from CreateFile()
                    64*1024)    # Integer: number of bytes to be read / ReadBuffer: where the ReadFile operation shoud place the data
                msg = msg.decode()
                logging.info(f'message: {msg}')
                if 'stop' in msg:
                    logging.info('Stop on client')
                    loop = False

        except pywintypes.error as e:
            if e.args[0] == 2:
                logging.warning('no pipe, trying again in a sec')
                time.sleep(1)
            elif e.args[0] == 10:
                logging.error('broken pipe, quit pipe')
                quit = True


if __name__ == '__main__':
    pipe_client()
