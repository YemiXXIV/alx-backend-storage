#!/usr/bin/env python3
"""
To update a topic in document
"""
from pymongo import MongoClient


def update_topics(mongo_collection, name, topics):
    """
    update a topic in document
    """
    mongo_collection.update_many(
      {'name': name},
      {'$set': {'topics': topics}}
    )
