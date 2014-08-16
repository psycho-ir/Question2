__author__ = 'soroosh'
import xml.etree.ElementTree as ET


# with open("../inputs/inputs/sample_input.txt", 'r') as f:
# for line in f:
# print line

doc = ET.parse("../inputs/inputs/sample_input.xml")
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
print list


