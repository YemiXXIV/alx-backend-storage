#!/usr/bin/env python3
"""
list all documents of a mongodb
database collection
"""
from pymongo import MongoClient


def list_all(mongo_collection):
    """
    list all documents of a mongodb
    database collection
    """
    documents = mongo_collection.find()
    return list(documents)
