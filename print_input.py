import time
import sys
import logging

logging.basicConfig(level=logging.INFO)

# loop = True
# while loop:
#     _ = sys.stdin.readline()
#     # _ = input()
#     print(_)
#     logging.info(f'{__file__}: {_}')
#     # sys.stdout = _
#     time.sleep(3)
#     if _ == 'stop':
#         loop = False
#         print('Going to exit the programming')
#         logging.info('Going to exit the programming')


def print_(value):
    # print(value)
    logging.info(value)


if __name__ == '__main__':
    _ = sys.stdin.readline()
    _ = _ + ' modified'
    # print_(_)
    logging.info(_)
    print(_)


# _ = sys.stdin.readline()
# print(_)
# logging.info(f'{__file__}: {_}')