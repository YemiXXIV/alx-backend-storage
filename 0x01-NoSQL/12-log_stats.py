#!/usr/bin/env python3
"""
To get log of nginx from mongodb
"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient()
    collection = client.logs.nginx

    print(f"{collection.count_documents({})} logs")
    print(f"Methods:")
    print(f"\tmethod GET: {collection.count_documents({'method': 'GET'})}")
    print(f"\tmethod POST: {collection.count_documents({'method': 'POST'})}")
    print(f"\tmethod PUT: {collection.count_documents({'method': 'PUT'})}")
    print(f"\tmethod PATCH: {collection.count_documents({'method': 'PATCH'})}")
    count_del = collection.count_documents({'method': 'DELETE'})
    print(f"\tmethod DELETE: {count_del}")
    count_stats = {'$and': [{'method': 'GET'}, {'path': '/status'}]}
    print(f"{collection.count_documents(count_stats)} status check")
