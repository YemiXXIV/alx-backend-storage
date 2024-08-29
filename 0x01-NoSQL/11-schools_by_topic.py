#!/usr/bin/env python3
"""
To search by given value
"""
from pymongo import MongoClient


def schools_by_topic(mongo_collection, topic):
    """
    search by value
    """
    document_topic = mongo_collection.find({'topics': topic})

    return list(document_topic)
