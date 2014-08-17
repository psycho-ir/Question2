from src.repository import persist_bulk
import multiprocessing
from multiprocessing.queues import Empty

__author__ = 'Ebrahimi'
from itertools import islice
import logging


# def read_file(path, file_name, file_extension):
# def read_file(q):
# try:
# item = q.get_nowait()
# except Empty as e:
# logging.info('No task for me :(')
#         return
#     logging.basicConfig(level=logging.INFO)
#     file_extension = item[2]
#
#     input_file = open(item[0] + item[1] + "." + file_extension, 'r')
#     line_count = 400000
#     while True:
#         list_of_dic_dep = []
#         list_of_dic_pay = []
#         list_of_dic_trans = []
#         slice = islice(input_file, line_count)
#
#         for l in slice:
#             dic = {}
#             if file_extension == 'txt':
#                 rec = l.split(' ')
#
#             if rec[0] in ('Deposit', 'deposit'):
#                 # dic['type'] = 'Deposit'
#                 dic['acc1'] = rec[1]
#                 dic['amnt'] = float(rec[2].strip())
#                 list_of_dic_dep.append(dic)
#                 continue
#             if rec[0] in ('Payment', 'payment'):
#                 # dic['type'] = 'Payment'
#                 dic['acc1'] = rec[1]
#                 dic['amnt'] = float(rec[2].strip())
#                 list_of_dic_pay.append(dic)
#                 continue
#             if rec[0] in ('Transfer', 'transfer'):
#                 # dic['type'] = 'Transfer'
#                 dic['acc1'] = rec[1]
#                 dic['acc2'] = rec[4]
#                 dic['amnt'] = float(rec[2].strip())
#                 list_of_dic_trans.append(dic)
#                 continue
#         if len(list_of_dic_pay) == 0 and len(list_of_dic_dep) == 0 and len(list_of_dic_trans) == 0:
#             break;
#         persist_bulk(list_of_dic_pay, list_of_dic_dep, list_of_dic_trans)

def read_file(q):
    try:
        item = q.get_nowait()
        path = item[0]
        file_name = item[1]
        file_extension = item[2]
    except Empty as e:
        logging.info('No task for me :(')
        return
    logging.basicConfig(level=logging.INFO)
    input_file = open(path + file_name + "." + file_extension, 'r')
    if file_extension == 'txt' and read_file_txt(input_file) == True:
        logging.info("read txt file and insert to db ")
    if file_extension == 'csv' and read_file_csv(input_file) == True:
        logging.info("read csv file and insert to db ")
    if file_extension == 'xml' and read_file_xml(input_file) == True:
        logging.info("read xml file and insert to db ")
    if file_extension == 'json' and read_file_json(input_file) == True:
        logging.info("read json file and insert to db ")


def read_file_json(input_file):
    line_count = 200000
    transactions_tag = False
    deposit_tag = False
    payment_tag = False
    transfer_tag = False
    dic = {}
    list_of_dic_dep = []
    list_of_dic_pay = []
    list_of_dic_trans = []
    first_json_file = False
    first_braket = False
    end_json_file = False
    str_json = ''
    while True:

        slice = islice(input_file, line_count)

        for l in slice:

            if first_braket or l.find('[') > -1:
                first_braket = True
                str_json += l
                if str_json.find(']') > -1:
                    print str_json[str_json.find('['):str_json.find(']') + 1]


def read_file_xml(input_file):
    line_count = 200000
    transactions_tag = False
    deposit_tag = False
    payment_tag = False
    transfer_tag = False
    dic = {}
    list_of_dic_dep = []
    list_of_dic_pay = []
    list_of_dic_trans = []
    while True:

        slice = islice(input_file, line_count)

        # if len(dic) > 0:

        for l in slice:
            if l.find('version') != -1:
                continue

            if l.find('<transactions>') > -1 or transactions_tag:
                transactions_tag = True
                if l.find('<deposit>') > -1 or deposit_tag:
                    deposit_tag = True
                    if l.find('<account_id>') > -1 and l.find('</account_id>') > -1:
                        dic['acc1'] = l.replace('<account_id>', '').replace('</account_id>', '').strip()
                    if l.find('<amount>') > -1 and l.find('</amount>') > -1:
                        dic['amnt'] = float(l.replace('<amount>', '').replace('</amount>', '').strip())
                    if l.find('</deposit>') > -1:
                        deposit_tag = False
                        list_of_dic_dep.append(dic)
                        dic = {}
                if l.find('<payment>') > -1 or payment_tag:
                    payment_tag = True
                    if l.find('<account_id>') > -1 and l.find('</account_id>') > -1:
                        dic['acc1'] = l.replace('<account_id>', '').replace('</account_id>', '').strip()
                    if l.find('<amount>') > -1 and l.find('</amount>') > -1:
                        dic['amnt'] = float(l.replace('<amount>', '').replace('</amount>', '').strip())
                    if l.find('</payment>') > -1:
                        payment_tag = False
                        list_of_dic_pay.append(dic)
                        dic = {}
                if l.find('<transfer>') > -1 or transfer_tag:
                    transfer_tag = True
                    if l.find('<from>') > -1 and l.find('</from>') > -1:
                        dic['acc1'] = l.replace('<from>', '').replace('</from>', '').strip()
                    if l.find('<to>') > -1 and l.find('</to>') > -1:
                        dic['acc2'] = l.replace('<to>', '').replace('</to>', '').strip()
                    if l.find('<amount>') > -1 and l.find('</amount>') > -1:
                        dic['amnt'] = float(l.replace('<amount>', '').replace('</amount>', '').strip())
                    if l.find('</transfer>') > -1:
                        transfer_tag = False
                        list_of_dic_trans.append(dic)
                        dic = {}
                if l.find('</transactions>') > -1:
                    transactions_tag = False
                    persist_bulk(list_of_dic_pay, list_of_dic_dep, list_of_dic_trans)
                    print list_of_dic_dep
                    print list_of_dic_pay
                    print list_of_dic_trans
                    return True
    if len(list_of_dic_pay) > 0 and len(list_of_dic_dep) > 0 and len(list_of_dic_trans) > 0:
        print len(list_of_dic_dep)
        print len(list_of_dic_pay)
        print len(list_of_dic_trans)
        persist_bulk(list_of_dic_pay, list_of_dic_dep, list_of_dic_trans)
        list_of_dic_dep = []
        list_of_dic_pay = []
        list_of_dic_trans = []


def read_file_csv(input_file):
    line_count = 200000
    while True:
        list_of_dic_dep = []
        list_of_dic_pay = []
        list_of_dic_trans = []
        slice = islice(input_file, line_count)

        for l in slice:
            dic = {}
            rec = l.split(',')
            if len(rec) < 2:
                continue
            if rec[0] == 'From':
                continue
            if rec[0] == '':
                # deposit
                dic['acc1'] = rec[1]
                dic['amnt'] = float(rec[2].strip())
                list_of_dic_dep.append(dic)
                continue
            if rec[1] == '':
                # payment
                dic['acc1'] = rec[0]
                dic['amnt'] = float(rec[2].strip())
                list_of_dic_pay.append(dic)
                continue
            if rec[0] != '' and rec[1] != '' and rec[2] != '':
                dic['acc1'] = rec[0]
                dic['acc2'] = rec[1]
                dic['amnt'] = float(rec[2].strip())
                list_of_dic_trans.append(dic)
                continue
        if len(list_of_dic_pay) == 0 and len(list_of_dic_dep) == 0 and len(list_of_dic_trans) == 0:
            break;
        persist_bulk(list_of_dic_pay, list_of_dic_dep, list_of_dic_trans)
    return True


def read_file_txt(input_file):
    line_count = 200000
    while True:
        list_of_dic_dep = []
        list_of_dic_pay = []
        list_of_dic_trans = []
        slice = islice(input_file, line_count)

        for l in slice:
            dic = {}
            rec = l.split(' ')

            if rec[0] in ('Deposit', 'deposit'):
                # deposit
                dic['acc1'] = rec[1]
                dic['amnt'] = float(rec[2].strip())
                list_of_dic_dep.append(dic)
                continue
            if rec[0] in ('Payment', 'payment'):
                # payment
                dic['acc1'] = rec[1]
                dic['amnt'] = float(rec[2].strip())
                list_of_dic_pay.append(dic)
                continue
            if rec[0] in ('Transfer', 'transfer'):
                dic['acc1'] = rec[1]
                dic['acc2'] = rec[4]
                dic['amnt'] = float(rec[2].strip())
                list_of_dic_trans.append(dic)
                continue
        if len(list_of_dic_pay) == 0 and len(list_of_dic_dep) == 0 and len(list_of_dic_trans) == 0:
            break;
        persist_bulk(list_of_dic_pay, list_of_dic_dep, list_of_dic_trans)
    return True


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    q = multiprocessing.Queue()
    ps = [multiprocessing.Process(target=read_file, args=(q,), name="P-" + str(i)) for i in xrange(multiprocessing.cpu_count())]

    input_path_list = ["../inputs/sort_problem/sample_input_2.txt", "../inputs/sort_problem/sample_input_1.txt", "../inputs/sort_problem/small.txt"]
    # sort_transactions(input_path_list, 'aaa')
