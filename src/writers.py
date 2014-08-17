__author__ = 'soroosh'
import json
from xml.dom import minidom
import operator

import xml.etree.ElementTree as ET


class XMLWriter:
    def __init__(self):
        self.result = ''

    def write(self, text):
        self.result += text


def _prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    w = XMLWriter()
    ET.ElementTree(elem).write(w)
    reparsed = minidom.parseString(w.result)
    return reparsed.toprettyxml(indent="  ")


def _xml_writer(list, output):
    doc = ET.Element("accounts_delta")
    for rec in range(len(list)):
        doc1 = ET.SubElement(doc, "account")
        field1 = ET.SubElement(doc1, "id")
        field1.text = list[rec]['acc_no']
        field2 = ET.SubElement(doc1, "amount")
        field2.text = str(float(list[rec]['remain']))

    output.write(_prettify(doc))


def _json_writer(list, output):
    n_list = []
    for rec in range(len(list)):
        dic = {}
        new_dic = {}
        dic['account_id'] = list[rec]['acc_no']
        dic['amount'] = list[rec]['remain']
        n_list.append(sorted(dic.iteritems(), key=operator.itemgetter(1), reverse=True))
    new_dic['accounts_delta'] = n_list
    json.dump(new_dic, output)


def _txt_writer(list, output):
    for rec in range(len(list)):
        output.write(list[rec]['acc_no'] + ' ' + str(float(list[rec]['remain'])) + "\n")


def _csv_writer(list, output):
    output.write('ID' + ',' + ' Amount' + "\n")
    _txt_writer(list, output)


__writers = {
    'xml': _xml_writer,
    'json': _json_writer,
    'csv': _csv_writer,
    'txt': _txt_writer
}


def write(file_name, list):
    with open(file_name, 'w') as output:
        extension = file_name.split('.')[-1]
        __writers[extension](list,output)

