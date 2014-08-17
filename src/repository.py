__author__ = 'soroosh'
from src import config

from pymongo import MongoClient

client = MongoClient(config.MONGODB['host'], config.MONGODB['port'])
db = client[config.MONGODB['db']]
payment_collection = db[config.MONGODB['payment_collection']]
deposit_collection = db[config.MONGODB['deposit_collection']]
transfer_collection = db[config.MONGODB['transfer_collection']]


def persist_bulk(payment_list, deposit_list, transfer_list):
    print 'persisting... Number of payments:%s , Number of deposits: %s , Number of transfers: %s' % (len(payment_list), len(deposit_list), len(transfer_list))
    if len(payment_list) > 0:
        payment_collection.insert(payment_list, manipulate=False, check_keys=False)
    if len(deposit_list) > 0:
        deposit_collection.insert(deposit_list, manipulate=False, check_keys=False)
    if len(transfer_list) > 0:
        transfer_collection.insert(transfer_list, manipulate=False, check_keys=False)


def create_indexes():
    payment_collection.ensure_index('amnt')
    deposit_collection.ensure_index('amnt')
    transfer_collection.ensure_index('amnt')


def read_all_payments():
    return payment_collection.find({}).sort('amnt', -1)


def read_all_deposits():
    return deposit_collection.find({}).sort('amnt', -1)


def read_all_transfers():
    return transfer_collection.find({}).sort('amnt', -1)

