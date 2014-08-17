__author__ = 'soroosh'
from src.repository import persist_bulk
from multiprocessing.queues import Empty

from itertools import islice
import logging

line_count = 200


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
    if file_extension == 'txt':
        read_file_txt(input_file)
        logging.info("read txt file and insert to db ")
    if file_extension == 'csv':
        read_file_csv(input_file)
        logging.info("read csv file and insert to db ")
    if file_extension == 'xml':
        read_file_xml(input_file)
        logging.info("read xml file and insert to db ")
    if file_extension == 'json':
        read_file_json(input_file)
        logging.info("read json file and insert to db ")

def read_file_json(input_file):
    list_of_dic_dep = []
    list_of_dic_pay = []
    list_of_dic_trans = []
    first_braket = False
    first_kroshe = False
    str_json = ''
    dic = {}
    while True:

        slice = islice(input_file, line_count)

        for l in slice:
            if l.find('[') > -1:
                l = l[l.find('[') + 1:]
                first_braket = True
            if first_braket or l.find('[') > -1:
                if l.find(']') == -1:
                    if first_kroshe or l.find('{') > -1:
                        first_kroshe = True
                        str_json += l.strip()
                        if str_json.find('}') > -1:
                            tmp_str_json = str_json[str_json.find('{') + 1:str_json.find('}')]
                            str_json = str_json[str_json.find('}') + 1:]
                            tmp_str_json = tmp_str_json.replace('\'\'', '').replace('\'\'', '').replace('\"',
                                                                                                        '').replace(
                                '\"',
                                '').replace(
                                '{', '').replace('}', '')
                            # for rec in tmp_str_json.split('type'):
                            if tmp_str_json.find('deposit') > -1:
                                for rec1 in tmp_str_json.split(','):
                                    if rec1.find('account_id:') > -1:
                                        dic['acc1'] = rec1.split('account_id:')[1]
                                    if rec1.find('amount:') > -1:
                                        dic['amnt'] = float(rec1.split('amount:')[1])
                                list_of_dic_dep.append(dic)
                                dic = {}
                                first_kroshe = False
                                continue
                            if tmp_str_json.find('payment') > -1:
                                for rec1 in tmp_str_json.split(','):
                                    if rec1.find('account_id:') > -1:
                                        dic['acc1'] = rec1.split('account_id:')[1]
                                    if rec1.find('amount:') > -1:
                                        dic['amnt'] = float(rec1.split('amount:')[1])
                                list_of_dic_pay.append(dic)
                                dic = {}
                                first_kroshe = False
                                continue
                            if tmp_str_json.find('transfer') > -1:
                                for rec1 in tmp_str_json.split(','):
                                    if rec1.find('from:') > -1:
                                        dic['acc1'] = rec1.split('from:')[1]
                                    if rec1.find('to:') > -1:
                                        dic['acc2'] = rec1.split('to:')[1]
                                    if rec1.find('amount:') > -1:
                                        dic['amnt'] = float(rec1.split('amount:')[1])
                                list_of_dic_trans.append(dic)
                                dic = {}
                                first_kroshe = False
                                continue
                            else:
                                continue
                else:
                    persist_bulk(list_of_dic_pay, list_of_dic_dep, list_of_dic_trans)
                    return
        persist_bulk(list_of_dic_pay, list_of_dic_dep, list_of_dic_trans)
        list_of_dic_dep = []
        list_of_dic_pay = []
        list_of_dic_trans = []


# def read_file_json(input_file):
#     list_of_dic_dep = []
#     list_of_dic_pay = []
#     list_of_dic_trans = []
#     first_braket = False
#     str_json = ''
#     dic = {}
#     while True:
#         slice = islice(input_file, line_count)
#         for l in slice:
#             if first_braket or l.find('[') > -1:
#                 first_braket = True
#                 if l.find(']') == -1:
#                     if l.find('{') > -1:
#                         str_json += l.strip()
#                         if str_json.find('}') > -1:
#                             tmp_str_json = str_json[str_json.find('{') + 1:str_json.find('}')]
#                             str_json = str_json[str_json.find('}') + 1:]
#                             tmp_str_json = tmp_str_json.replace('\'\'', '').replace('\'\'', '').replace('\"',
#                                                                                                         '').replace(
#                                 '\"',
#                                 '').replace(
#                                 '{', '').replace('}', '')
#                             # for rec in tmp_str_json.split('type'):
#                             if tmp_str_json.find('deposit') > -1:
#                                 for rec1 in tmp_str_json.split(','):
#                                     if rec1.find('account_id:') > -1:
#                                         dic['acc1'] = rec1.split('account_id:')[1]
#                                     if rec1.find('amount:') > -1:
#                                         dic['amnt'] = float(rec1.split('amount:')[1])
#                                 list_of_dic_dep.append(dic)
#                                 dic = {}
#                                 continue
#                             if tmp_str_json.find('payment') > -1:
#                                 for rec1 in tmp_str_json.split(','):
#                                     if rec1.find('account_id:') > -1:
#                                         dic['acc1'] = rec1.split('account_id:')[1]
#                                     if rec1.find('amount:') > -1:
#                                         dic['amnt'] = float(rec1.split('amount:')[1])
#                                 list_of_dic_pay.append(dic)
#                                 dic = {}
#                                 continue
#                             if tmp_str_json.find('transfer') > -1:
#                                 for rec1 in tmp_str_json.split(','):
#                                     if rec1.find('from:') > -1:
#                                         dic['acc1'] = rec1.split('from:')[1]
#                                     if rec1.find('to:') > -1:
#                                         dic['acc2'] = rec1.split('to:')[1]
#                                     if rec1.find('amount:') > -1:
#                                         dic['amnt'] = float(rec1.split('amount:')[1])
#                                 list_of_dic_trans.append(dic)
#                                 dic = {}
#                                 continue
#                             else:
#                                 continue
#                 else:
#                     persist_bulk(list_of_dic_pay, list_of_dic_dep, list_of_dic_trans)
#                     return
#         persist_bulk(list_of_dic_pay, list_of_dic_dep, list_of_dic_trans)
#         list_of_dic_dep = []
#         list_of_dic_pay = []
#         list_of_dic_trans = []


def read_file_xml(input_file):
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
                    return
        if len(list_of_dic_pay) > 0 and len(list_of_dic_dep) > 0 and len(list_of_dic_trans) > 0:
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
            if len(rec) < 2:
                continue
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
                # transfer
                dic['acc1'] = rec[1]
                dic['acc2'] = rec[4]
                dic['amnt'] = float(rec[2].strip())
                list_of_dic_trans.append(dic)
                continue
        if len(list_of_dic_pay) == 0 and len(list_of_dic_dep) == 0 and len(list_of_dic_trans) == 0:
            break;
        persist_bulk(list_of_dic_pay, list_of_dic_dep, list_of_dic_trans)
    return True
