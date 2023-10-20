#!/usr/bin/env python3

"""
    a script that provides some stats about Nginx logs stored in MongoDB
    Database: logs
    Collection: nginx
    Display (same as the example):
    first line: x logs where x is the number of documents in this collection
    second line: Methods: 5 lines with the number of documents with the
    method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    one line with the number of documents with: method=GET path=/status
"""

from pymongo import MongoClient

methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

my_client = MongoClient('mongodb://127.0.0.1:27017')
my_database = my_client['logs']
my_nginx = my_database['nginx']

print("{} logs".format(my_nginx.count_documents({})))

for method in methods:
    print(
            "\tmethod {}: {}".format(
                method, my_nginx.count_documents({"method": method}))
            )
    print(
            "{} status check".format(
                my_nginx.count_documents({"method": "GET", "path": "/status"})
                )
            )


if __name__ == "__main__":
    stats_logs()
