__author__ = 'soroosh'


def variz(acc_no, amnt):
    array = {}
    array['Deposit'] = 'Deposit'
    array['acc_no'] = acc_no
    array['amnt'] = amnt
    return array


def bardasht(acc_no, amnt):
    array = {}
    array['Payment'] = 'Payment'
    array['acc_no'] = acc_no
    array['amnt'] = -amnt
    return array

def add_acc_no_to_list(list, acc_no):
    is_exsit = False
    gardesh = {}
    for rec in range(len(list)):
        if list[rec]['acc_no'] == acc_no:
            is_exsit = True
            return False
    gardesh['acc_no'] = acc_no
    gardesh['bed'] = 0
    gardesh['bes'] = 0
    gardesh['remain'] = 0
    return list.append(gardesh)
