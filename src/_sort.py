__author__ = 'Ebrahimi'
from itertools import islice
import logging
from multiprocessing import Pool, Process
from multiprocessing.queues import Queue, Empty
import time

exitFlag = 0
SORT_IN_ADDRESS = '../inputs/sort_problem/'
SORT_OUT_ADDRESS = '../outputs/sort_problem/'

BLOCK_SIZE = (10 * 1024 * 1024 * 1024) - 100


def getSize(fileobject):
    fileobject.seek(0, 2)  # move the cursor to the end of the file
    size = fileobject.tell()
    return size


def produce_chunks(q):
    logging.basicConfig(level=logging.INFO)
    input_file = open(SORT_IN_ADDRESS + 'sample_input.txt', 'r')
    i = 0
    while True:
        i += 1
        flag = False
        with open(SORT_OUT_ADDRESS + "sample_output_" + str(i) + ".txt", 'a') as out_put:
            for l in islice(input_file, (200000)):
                if l:
                    flag = True
                    out_put.write(l)
                    # if out_put.tell() >= BLOCK_SIZE:
                    # print out_put.tell()
                    # break
            q.put(SORT_OUT_ADDRESS + "sample_output_" + str(i) + ".txt")
            logging.info("sample_output_" + str(i) + ".txt file name add to queue")
            if not flag:
                q.put("__end__")
                q.put("__end__")
                logging.info("token free")
                return


def consume(q):
    logging.basicConfig(level=logging.INFO)

    try:
        while True:
            print q.qsize()
            address_path = q.get(block=True, timeout=5)
            print address_path
            if address_path == "__end__":
                print 'end read'
                break

            list_line = open(address_path, 'r').read()
            logging.info("sample_output_" + address_path + " read from queue")

            while True:
                list_of_pay, list_of_dep, list_of_trns = add_to_list_part(list_line)
                if len(list_of_pay) > 0 or len(list_of_dep) > 0 or len(list_of_trns) > 0:

                    out_put = open(SORT_OUT_ADDRESS + "/sorted/sort_output_" + address_path.split('/')[-1], 'a')
                    for rec in range(len(list_of_pay)):
                        out_put.write(list_of_pay[rec] + "\n")
                    for rec in range(len(list_of_dep)):
                        out_put.write(list_of_dep[rec] + "\n")
                    for rec in range(len(list_of_trns)):
                        out_put.write(list_of_trns[rec] + "\n")
                    break
                break

    except Empty as e:
        logging.info("queue empty now...")
        return


def add_to_list_part(input):
    list_of_pay = []
    list_of_dep = []
    list_of_trns = []
    rows = input.split('\n')
    for r in rows:
        row = r.replace('\n', '').split(' ')
        for indx in range(len(row)):
            if row[indx] == 'Payment':
                list_of_pay.append(r.replace('\n', ''))
                break
            if row[indx] == 'Deposit':
                list_of_dep.append(r.replace('\n', ''))
                break
            if row[indx] == 'Transfer':
                list_of_trns.append(r.replace('\n', ''))

    sort(list_of_pay, r.replace('\n', ''), 2)
    sort(list_of_dep, r.replace('\n', ''), 2)
    sort(list_of_trns, r.replace('\n', ''), 2)
    return (list_of_pay, list_of_dep, list_of_trns)


def sort(list, item, index_of_list):
    list.sort(key=lambda i: float(i.split(' ')[index_of_list]), reverse=True)


class Token:
    def __init__(self):
        self.release = False


q = Queue(maxsize=0)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info("starting ...")
    p1 = Process(target=produce_chunks, args=(q,), name="produce_chunks")
    p2 = Process(target=consume, args=(q,), name="consumer-1")
    p3 = Process(target=consume, args=(q,), name="consumer-2")
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    print 'p1 joined'
    p2.join()
    print 'p2 joined'
    p3.join()
    print 'p3 joined'