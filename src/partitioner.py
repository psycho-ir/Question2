__author__ = 'soroosh'
import json
from src.repository import read_all_payments, read_all_deposits, read_all_transfers, create_indexes
MAX_SIZE = 5 * 1024 * 1024 - 100

pay_cursor = read_all_payments()
deposit_cursor = read_all_deposits()
transfer_cursor = read_all_transfers()

txt_template = "%s %s %s \r\n"
transfer_template = "%s %s %s > %s\r\n"


def _txt_writer(list_item, type):
    result = []
    for item in list_item:
        if type == 'Transfer':
            result.append(transfer_template % ('Transfer', item['acc1'], item['amnt'], item['acc2'].strip()))
        else:
            result.append(txt_template % (type, item['acc1'], item['amnt']))
    return ''.join(result)


def _csv_writer(list_item, type):
    result = ['From, To, Amount']
    for item in list_item:
        if type == 'Transfer':
            result.append('%s,%s,%s' % (item['acc1'].strip(), item['acc2'].strip(), item['amnt']))
        elif type == 'Deposit':
            result.append('%s,%s,%s' % ('', item['acc1'].strip(), item['amnt']))
        else:
            result.append('%s,%s,%s' % (item['acc1'].strip(), '', item['amnt']))

    return '\r\n'.join(result)


class XMLWriter:
    def __init__(self):
        self.result = ''

    def write(self, text):
        self.result += text


def _xml_writer(list_item, type):
    result = []
    result.append('<transactions>')
    for item in list_item:

        if type == 'Transfer':
            result.append('<transfer><from>%s</from><to>%s</to><amount>%s</amount></transfer>' % (item['acc1'].strip(), item['acc2'].strip(), str(item['amnt'])))
        else:
            result.append('<%s><account_id>%s</account_id><amount>%s</amount></%s>' % (type, item['acc1'].strip(), str(item['amnt']), type))
    result.append('</transaction>')
    return '\r\n'.join(result)


def _json_writer(list_item, type):
    root = {'transactions': []}
    for item in list_item:
        if type == "Transfer":
            root['transactions'].append({'type': type, 'from': item['acc1'].strip(), 'to': item['acc2'].strip(), 'amount': item['amnt']})
        else:
            root['transactions'].append({'type': type, 'account_id': item['acc1'].strip(), 'amount': item['amnt']})

    return json.dumps(root)


writers = {'txt': _txt_writer,
           'xml': _xml_writer,
           'json': _json_writer,
           'csv': _csv_writer}


def _create_file(name, list, extension, type):
    with  open('../sort_result/' + name, 'w') as f:
        f.write(writers[extension](list, type))
    print "File %s created" % name


def create_payment_files(counter, output_basename, extension):
    size = 0
    result_list = []
    stopped = False

    while size < MAX_SIZE and not stopped:
        try:
            pay_item = next(pay_cursor)
        except StopIteration as e:
            stopped = True
        if not stopped:
            result = txt_template % ('Payment', pay_item['acc1'], pay_item['amnt'])
            result_list.append(pay_item)
            size += len(result)
    else:
        _create_file(output_basename + '_payment_' + str(counter) + '.' + extension, result_list, extension, 'Payment')
        if not stopped:
            create_payment_files(counter + 1, output_basename, extension)


def create_deposit_files(counter, output_basename, extension):
    size = 0
    result_list = []
    stopped = False

    while size < MAX_SIZE and not stopped:
        try:
            deposit_item = next(deposit_cursor)
        except StopIteration as e:
            stopped = True
        if not stopped:
            result = txt_template % ('Deposit', deposit_item['acc1'], deposit_item['amnt'])
            result_list.append(deposit_item)
            size += len(result)
    else:
        _create_file(output_basename + '_deposit_' + str(counter) + '.' + extension, result_list, extension, 'Deposit')
        if not stopped:
            create_deposit_files(counter + 1, output_basename, extension)


def create_transfer_files(counter, output_basename, extension):
    size = 0
    result_list = []
    stopped = False

    while size < MAX_SIZE and not stopped:
        try:
            transfer_item = next(transfer_cursor)
        except StopIteration as e:
            stopped = True
        if not stopped:
            result = transfer_template % ('Transfer', transfer_item['acc1'].strip(), transfer_item['amnt'], transfer_item['acc2'].strip())
            result_list.append(transfer_item)
            size += len(result)
    else:
        _create_file(output_basename + '_transfer_' + str(counter) + '.' + extension, result_list, extension, 'Transfer')
        if not stopped:
            create_transfer_files(counter + 1, output_basename, extension)







