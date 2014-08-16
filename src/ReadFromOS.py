import json
from pprint import pprint
from xml.dom import minidom
import exceptions
import operator
from src.readers import _xml_reader, _json_reader, _csv_reader

__author__ = 'soroosh'
import xml.etree.ElementTree as ET

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    w = XMLWriter()
    rough_string = ET.ElementTree(elem).write(w)
    reparsed = minidom.parseString(w.result)
    return reparsed.toprettyxml(indent="  ")


class ReadFile:
    def analysis_transaction(self, input_file, output_file):
        try:
            list = []
            list_acc_no = []
            list_line = []
            list_line = read_file(input_file)
            file_extension = input_file.split('.')[-1]

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
            output_file(output_file, newlist, file_extension)

        except Exception as e:
            print e.message + '  ->  ' + 'File not found'

        return False


if __name__ == '__main__':
    file_name = "sample_input.json"
    ReadFile().analysis_transaction(input_file=file_name)




