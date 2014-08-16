import json
import xml.etree.ElementTree as ET

__author__ = 'soroosh'


def _json_reader(json_file):
    list = []
    try:
        json_read = json.loads(json_file.read())
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


def _xml_reader(xml_file):
    doc = ET.parse(xml_file)
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


def _csv_reader(csv_file):
    list_line = []
    for line in csv_file:
        list_line.append(line.strip())
    list = []
    for rec in range(len(list_line)):
        str = ''
        if rec > 0:
            splitted_line = list_line[rec].split(",")
            if splitted_line[0] == '':
                str += 'Deposit'
                str += ' '
                str += splitted_line[1]
                str += ' '
                str += splitted_line[2]
                list.append(str)
                continue
            if splitted_line[1] == '':
                str += 'Payment'
                str += ' '
                str += splitted_line[0]
                str += ' '
                str += splitted_line[2]
                list.append(str)
                continue
            else:
                acc_no1 = splitted_line[0]
                acc_no2 = splitted_line[1]
                amnt = splitted_line[2]

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


def read_file(input_file):
    file_open = open(input_file, 'r')
    file_extension = input_file.split('.')[-1]

    if file_extension not in ('txt', 'json', 'csv', 'xml'):
        print 'file format not support'
        return False

    if file_extension == 'json':
        return _json_reader(file_open)
        if file_extension == 'xml':
            return _xml_reader(file_open)
    else:
        if file_extension == 'txt':
            for line in file_open:
                list_line = [line.replace("\n", "")]
            return list_line
        if file_extension == 'csv':
            return _csv_reader(file_open)