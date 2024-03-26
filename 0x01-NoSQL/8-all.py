#!/usr/bin/env python3
""" List all documents in a collection """


def list_all(mongo_collection):
    """ List all documents in MongoDB collection """
    documents = []
    for doc in mongo_collection.find():
        documents.append(doc)
    return documents
