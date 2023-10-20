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
ips = [
        "172.31.63.67", "172.31.2.14",
        "172.31.29.194", "69.162.124.230",
        "64.124.26.109", "64.62.224.29",
        "34.207.121.61", "47.88.100.4",
        "45.249.84.250", "216.244.66.228"
        ]

my_client = MongoClient('mongodb://127.0.0.1:27017')
my_database = my_client['logs']
my_nginx = my_database['nginx']

print("{} logs".format(my_nginx.count_documents({})))

print("Methods:")
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
print("IPs:")
for ip in ips:
    print(
            "\t{}: {}".format(
                ip, my_nginx.count_documents({"ip": ip})
                )
            )


if __name__ == "__main__":
    stats_logs()
