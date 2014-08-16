__author__ = 'soroosh'
from src.operations import variz, add_acc_no_to_list, bardasht
from src.readers import read_file
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


def sort_transactions(input_filelist, out_basename):
        #Not Completed
        pass

