import logging
import multiprocessing

__author__ = 'soroosh'
from src.operations import variz, add_acc_no_to_list, bardasht
from src.readers import read_file
from src.importer import read_file as rf
from src.writers import write


def analysis_transaction(input_file, output_file):
    try:
        list = []
        list_acc_no = []
        list_line = read_file(input_file)

        for rec1 in range(len(list_line)):
            row = list_line[rec1].split(' ')
            for indx in range(len(row)):
                if row[indx] == 'Deposit':
                    list.append(variz(row[indx + 1], long(float(row[indx + 2]))))
                    add_acc_no_to_list(list_acc_no, row[indx + 1])
                    break
                if row[indx] == 'Payment':
                    list.append(bardasht(row[indx + 1], long(float(row[indx + 2]))))
                    add_acc_no_to_list(list_acc_no, row[indx + 1])
                    break
                if row[indx] == 'Transfer':
                    add_acc_no_to_list(list_acc_no, row[indx + 1])
                    add_acc_no_to_list(list_acc_no, row[indx + 4])
                    list.append(bardasht(row[indx + 1], long(float(row[indx + 2]))))
                    list.append(variz(row[indx + 4], long(float(row[indx + 2]))))
                    break

        for var in range(len(list)):
            for var2 in range(len(list_acc_no)):
                if list[var]['acc_no'] == list_acc_no[var2]['acc_no']:
                    if list[var]['amnt'] > 0:
                        list_acc_no[var2]['bes'] = list[var]['amnt']
                        list_acc_no[var2]['remain'] = list_acc_no[var2]['remain'] + list[var]['amnt']
                    if list[var]['amnt'] < 0:
                        list_acc_no[var2]['bed'] = -list[var]['amnt']
                        list_acc_no[var2]['remain'] = list_acc_no[var2]['remain'] + (list[var]['amnt'])

        newlist = sorted(list_acc_no, key=lambda k: k['acc_no'])
        write(output_file, newlist)

    except Exception as e:
        raise e
        # print e.message + '  ->  ' + 'File not found'


import repository
import partitioner


def sort_transactions(input_path_list, output_basename):
    logging.basicConfig(level=logging.INFO)
    q = multiprocessing.Queue()
    ps = [multiprocessing.Process(target=rf, args=(q,), name="P-" + str(i)) for i in xrange(multiprocessing.cpu_count())]
    for path in input_path_list:
        file_name_by_ext = path.split("/")[-1]
        path_without_file = path.replace(file_name_by_ext, "")
        file_name = file_name_by_ext.split('.')[-2]
        file_extension = file_name_by_ext.split('.')[-1]
        # read_file(path_without_file, file_name, file_extension)
        q.put((path_without_file, file_name, file_extension,))
    map(lambda p: p.start(), ps)
    map(lambda p: p.join(), ps)
    # Now all transactoins are persisted in our repository
    # We create some index
    print "Creating Indexes on collections"
    repository.create_indexes()
    print "Indexes created..."
    print "Creating Deposit Files"
    extension = input_path_list[0].split('.')[-1]
    deposit_p = multiprocessing.Process(name="DEPOSIT-PROCESS", target=partitioner.create_deposit_files, args=(0, output_basename, extension))
    transfer_p = multiprocessing.Process(name="TRANSFER-PROCESS", target=partitioner.create_transfer_files, args=(0, output_basename, extension))
    payment_p = multiprocessing.Process(name="PAYMENT-PROCESS", target=partitioner.create_payment_files, args=(0, output_basename, extension))

    deposit_p.start()
    transfer_p.start()
    payment_p.start()
    deposit_p.join()
    transfer_p.join()
    payment_p.join()
    print "Now you can use your files"

