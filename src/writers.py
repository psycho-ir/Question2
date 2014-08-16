import json
from xml.dom import minidom
import operator

__author__ = 'soroosh'
import xml.etree.ElementTree as ET


class XMLWriter:
    def __init__(self):
        self.result = ''

    def write(self, text):
        self.result += text


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    w = XMLWriter()
    rough_string = ET.ElementTree(elem).write(w)
    reparsed = minidom.parseString(w.result)
    return reparsed.toprettyxml(indent="  ")


def write(file_name, list, extension):
    with open(file_name + '.' + extension, 'w') as output:
        if extension == 'xml':
            doc = ET.Element("accounts_delta")
            for rec in range(len(list)):
                doc1 = ET.SubElement(doc, "account")
                field1 = ET.SubElement(doc1, "id")
                field1.text = list[rec]['acc_no']
                field2 = ET.SubElement(doc1, "amount")
                field2.text = str(float(list[rec]['remain']))

            output.write(prettify(doc))
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
            json.dump(new_dic, output)
            return True

        if extension == 'csv':
            output.write('ID' + ',' + ' Amount' + "\n")
        for rec in range(len(list)):
            output.write(list[rec]['acc_no'] + ' ' + str(float(list[rec]['remain'])) + "\n")
        output.close()
        return True

