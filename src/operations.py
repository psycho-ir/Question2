__author__ = 'soroosh'


def variz(acc_no, amnt):
    result = {}
    result['Deposit'] = 'Deposit'
    result['acc_no'] = acc_no
    result['amnt'] = amnt
    return result


def bardasht(acc_no, amnt):
    result = {}
    result['Payment'] = 'Payment'
    result['acc_no'] = acc_no
    result['amnt'] = -amnt
    return result

def add_acc_no_to_list(list, acc_no):
    gardesh = {}
    for rec in range(len(list)):
        if list[rec]['acc_no'] == acc_no:
            return False
    gardesh['acc_no'] = acc_no
    gardesh['bed'] = 0
    gardesh['bes'] = 0
    gardesh['remain'] = 0
    return list.append(gardesh)
