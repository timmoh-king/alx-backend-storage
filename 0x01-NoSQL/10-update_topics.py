#!/usr/bin/env python3

"""
     function that changes all topics of a school doc based on the name
     Prototype: def update_topics(mongo_collection, name, topics):
     mongo_collection will be the pymongo collection object
     name (string) will be the school name to update
     topics (list of str) will be the list of topics approached in the sch
"""

def update_topics(mongo_collection, name, topics):
    """
        changes all topics of a school document based on the name:
    """
    result = mongo_collection.update_one({"name": name}, {"$set": {"topics" : topics}})
    return result
