#!/usr/bin/env python3
'''
PyMongo operations: finding documents
'''


def list_all(mongo_collection):
    ''' lists all documents in a collection '''
    result = mongo_collection.find()
    return result
