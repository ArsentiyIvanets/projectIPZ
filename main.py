from threading import Thread
from time import sleep

from DiscountsBot.bot import main
from parsers.atb_parser import get_parsed_atb


def control():
    main()
    while True:
        T2.join(10)
        sleep(120)


T1 = Thread(target=control)
T2 = Thread(target=get_parsed_atb)
T2.setDaemon(True)


if __name__ == '__main__':
    T1.start()
