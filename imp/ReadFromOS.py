import json
from pprint import pprint
from xml.dom import minidom
import exceptions
import operator

__author__ = 'Ebrahimi'
import os, sys
import xml.etree.ElementTree as ET


class XMLWriter:
    def __init__(self):
        self.result = ''

    def write(self, text):
        self.result += text


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


def read_file(input_file):
    file_open = open("../2/2/" + input_file, 'r')
    file_extension = input_file.split('.')[-1]

    if file_extension not in ('txt', 'json', 'csv', 'xml'):
        print 'file format not support'
        return False
    bool = True
    line_counter1 = 0
    step = 2
    line_counter2 = step

    list_line = []
    # while (bool):
    #
    # try:
    # linecount = file_open.readline()
    # # linecount = file_open.read().splitlines()[line_counter1:line_counter2];
    # if len(linecount) == 0:
    # bool = False
    # else:
    # list_line.append(linecount)
    # line_counter1 = line_counter2
    # line_counter2 += step
    # except:
    # bool = False
    # file_open.close()
    if file_extension == 'xml':
        return xml_reader(input_file)
    if file_extension == 'json':
        return json_reader(file_open)
    else:
        with file_open as f:
            for line in f:
                list_line.append(line.replace("\n", ""))
        if file_extension == 'txt':
            return list_line
        if file_extension == 'csv':
            return convert_csv_to_txt(list_line)


def json_reader(json_data):
    list = []
    try:
        json_read = json.loads(json_data.read())
        for line in json_read:

            for rec in range(len(json_read[line])):
                strr = ''
                if json_read[line][rec]['type'] == 'deposit':
                    strr += 'Deposit'
                    strr += ' '
                    strr += str(json_read[line][rec]['account_id'])
                    strr += ' '
                    strr += str(json_read[line][rec]['amount'])
                    list.append(strr)
                    continue
                if json_read[line][rec]['type'] == 'payment':
                    strr += 'Payment'
                    strr += ' '
                    strr += str(json_read[line][rec]['account_id'])
                    strr += ' '
                    strr += str(json_read[line][rec]['amount'])
                    list.append(strr)
                    continue
            else:

                acc_no1 = str(json_read[line][rec]['from'])
                acc_no2 = str(json_read[line][rec]['to'])
                amnt = str(json_read[line][rec]['amount'])

                strr += 'Payment'
                strr += ' '
                strr += acc_no1
                strr += ' '
                strr += amnt
                list.append(strr)
                strr = ''
                strr += 'Deposit'
                strr += ' '
                strr += acc_no2
                strr += ' '
                strr += amnt
                list.append(strr)
                continue

    except Exception as ee:
        print ee.message + " ==> " + 'json file error'
        return False
    return list


def xml_reader(input_file):
    doc = ET.parse("../2/2/" + input_file)
    root = doc.getroot()  # <--- this is the new line
    list = []
    for rec in range(len(root._children)):
        str = ''
        str1 = ''
        str2 = ''
        if root._children[rec].tag == 'deposit':
            str += 'Deposit'
            str += ' '
            for rec2 in root._children[rec]:
                if rec2.tag == 'account_id':
                    str += rec2.text
                    str += ' '
                    continue
                if rec2.tag == 'amount':
                    str += rec2.text
                    continue
            list.append(str)
            continue
        if root._children[rec].tag == 'payment':
            str += 'Payment'
            str += ' '
            for rec2 in root._children[rec]:
                if rec2.tag == 'account_id':
                    str += rec2.text
                    str += ' '
                    continue
                if rec2.tag == 'amount':
                    str += rec2.text
                    continue
            list.append(str)
            continue
        else:
            if root._children[rec].tag == 'transfer':
                for rec2 in root._children[rec]:
                    if rec2.tag == 'from':
                        str1 += 'Payment'
                        str1 += ' '
                        str1 += rec2.text
                        str1 += ' '
                        continue
                    if rec2.tag == 'to':
                        str2 += 'Deposit'
                        str2 += ' '
                        str2 += rec2.text
                        str2 += ' '
                        continue
                    if rec2.tag == 'amount':
                        str1 += rec2.text
                        str1 += ' '
                        list.append(str1)
                        str2 += rec2.text
                        str2 += ' '
                        list.append(str2)
                        continue
    return list


def convert_csv_to_txt(list_line):
    list = []
    for rec in range(len(list_line)):
        str = ''
        if rec > 0:
            split_file = list_line[rec].split(",")
            if split_file[0] == '':
                str += 'Deposit'
                str += ' '
                str += split_file[1]
                str += ' '
                str += split_file[2]
                list.append(str)
                continue
            if split_file[1] == '':
                str += 'Payment'
                str += ' '
                str += split_file[0]
                str += ' '
                str += split_file[2]
                list.append(str)
                continue
            else:
                acc_no1 = split_file[0]
                acc_no2 = split_file[1]
                amnt = split_file[2]

                str += 'Payment'
                str += ' '
                str += acc_no1
                str += ' '
                str += amnt
                list.append(str)
                str = ''
                str += 'Deposit'
                str += ' '
                str += acc_no2
                str += ' '
                str += amnt
                list.append(str)
                continue

    return list


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    w = XMLWriter()
    rough_string = ET.ElementTree(elem).write(w)
    reparsed = minidom.parseString(w.result)
    return reparsed.toprettyxml(indent="  ")


def output_file(list, extension):
    output_file = open("../2/2/my/sample_output." + extension, 'w')
    if extension == 'xml':
        doc = ET.Element("accounts_delta")
        for rec in range(len(list)):
            doc1 = ET.SubElement(doc, "account")
            field1 = ET.SubElement(doc1, "id")
            field1.text = list[rec]['acc_no']
            field2 = ET.SubElement(doc1, "amount")
            field2.text = str(float(list[rec]['remain']))

        output_file.write(prettify(doc))
        return True

    if extension == 'json':
        n_list = []
        for rec in range(len(list)):
            dic = {}
            new_dic = {}
            dic['account_id'] = list[rec]['acc_no']
            dic['amount'] = list[rec]['remain']
            n_list.append(sorted(dic.iteritems(), key=operator.itemgetter(1), reverse=True))
        new_dic['accounts_delta'] = n_list
        json.dump(new_dic, output_file)
        return True

    if extension == 'csv':
        output_file.write('ID' + ',' + ' Amount' + "\n")
    for rec in range(len(list)):
        output_file.write(list[rec]['acc_no'] + ' ' + str(float(list[rec]['remain'])) + "\n")
    output_file.close()
    return True


class ReadFile:
    def analysis_transaction(self, input_file):
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
            output_file(newlist, file_extension)

        except Exception as e:
            print e.message + '  ->  ' + 'File not found'

        return False


if __name__ == '__main__':
    # file_name = "sample_input.txt"
    # file_name = "sample_input.csv"
    # file_name = "sample_input.xml"
    file_name = "sample_input.json"
ReadFile().analysis_transaction(input_file=file_name)




