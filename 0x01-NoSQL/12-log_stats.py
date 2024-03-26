#!/usr/bin/env python3
""" Log stats from a collection """

from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient()
    nginx_collection = client.logs.nginx
    method_count = {"GET": 0, "POST": 0, "PUT": 0, "PATCH": 0, "DELETE": 0}
    methods = nginx_collection.find()
    for method in methods:
        if method.get("method") in method_count:
            method_count[method.get("method")] += 1
    print(f"{nginx_collection.count_documents({})} logs")
    print("Methods:")
    for method, count in method_count.items():
        print(f"\tmethod {method}: {count}")
    print(f"{nginx_collection.count_documents(
        {'method': 'GET', 'path': '/status'})
    } status check")
