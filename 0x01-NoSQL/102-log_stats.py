#!/usr/bin/python3
""" Log stats """
from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    print(f'{logs_collection.count_documents({})} logs')

    print('Methods:')
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = logs_collection.count_documents({'method': method})
        print(f'\tmethod {method}: {count}')

    print(f'{logs_collection.count_documents({"path": "/status"})} status check')

    print('IPs:')
    top_ips = logs_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    for ip in top_ips:
        print(f'\t{ip["_id"]}: {ip["count"]}')
